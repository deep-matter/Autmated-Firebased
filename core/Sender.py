import os
import pandas as pd
from tqdm import tqdm
import asyncio
from utlis import re_initialized_auth  # Fix the import statement
import shutil  # Import the shutil module

class Sender:
    def __init__(self, data_csv_path: str, authentication, config):
        self.data_csv_path = data_csv_path
        self.authentication = authentication
        self.queues = []  # Initializing three queues
        self.partition_name = os.path.splitext(os.path.basename(self.data_csv_path))[0]
        self.data = "./Data/"
        self.config = config
        self.path = self.data + self.partition_name

    async def re_auth(self, queue_index):
        auth = re_initialized_auth(self.config)
        if queue_index != 0:
            await asyncio.sleep(2)
            await self.process_queued_emails(queue_index=queue_index, auth=auth)

    async def send_email(self) -> None:
        #user_data = pd.read_csv(self.data_csv_path)
        for queue_index in range(1, 5):      
            if queue_index < 4 :
                await self.process_queue_email(queue_index)

            if queue_index == 4:
                await self.re_auth(queue_index=queue_index)
            
    async def process_queue_email(self, queue_index) -> None:
        data_part = pd.read_csv(f"{self.path}/part_{queue_index}.csv")
        for index, row in tqdm(data_part.iterrows(), total=len(data_part),
                               desc=f"Processing Sending Emails partition {queue_index}"):
            email_csv = row['Email']
            await asyncio.sleep(0.5)
            try:
                self.authentication.send_password_reset_email(email_csv)
                tqdm.write(f"Password reset email sent successfully to {email_csv}")
                await asyncio.sleep(1)
                data_part = data_part.drop(index)
                await asyncio.sleep(1)
            except Exception as e:
                error_message = str(e)
                if "QUOTA_EXCEEDED" in error_message:
                    self.queues.append(email_csv)
                    tqdm.write(f"Email queued for sending later (Queue {queue_index}): {email_csv}")
                    await asyncio.sleep(1)

        if queue_index == 3:
            self.save_queue_data(self.queues, self.data, self.partition_name, queue_index)
        
    async def process_queued_emails(self, queue_index, auth) -> None:
        unsent_email_queue = []
        unsent_email_queue_final= []
        queue_path = os.path.join(self.path, f"queue_{queue_index - 1}.csv")
        if os.path.exists(queue_path):
            queue = pd.read_csv(queue_path)
            await asyncio.sleep(0.5)
            if len(queue) > 1 :
                print(f"Start Queued Emails in Queue {queue_index - 1} left Email not sent are {len(queue)}")
                with tqdm(total=len(queue), desc=f"Processing Queued Emails in Queue {queue_index - 1}") as pbar:
                    for index , row in queue.iterrows():
                        email = row['Email']
                        pbar.update(1)
                        await asyncio.sleep(1)
                        try:
                            auth.send_password_reset_email(email)
                            tqdm.write(f"Password reset email sent successfully to {email}")
                            queue = queue.drop(index)
                            await asyncio.sleep(0.5)

                        except Exception as error:
                            error_message = str(error)
                            if "QUOTA_EXCEEDED" in error_message:
                                unsent_email_queue.append(email)
                                tqdm.write(f"Email queued for unsent Emails: {email}")
                                await asyncio.sleep(2)

                    pbar.close()
                #queue_index = 4
                self.save_queue_data(unsent_email_queue, self.data, self.partition_name, (queue_index))
            else:
                print("Done Queued Emails sent to the inbox")

            print(f"Freeze Queue {queue_index - 1} the Auth for a period of time")
            await asyncio.sleep(1)

            if queue_index == 4:
                last_queue_path = os.path.join(self.path, f"queue_{queue_index}.csv")
                last_queue = pd.read_csv(last_queue_path)
                if len(last_queue) > 1:
                    print(f"Start Queued Emails in Queue 5 left Email not sent are {len(last_queue)}")
                    with tqdm(total=len(last_queue), desc=f"Processing Queued Emails in Queue {queue_index}") as pbar:
                        for index , row in last_queue.iterrows():
                            email = row['Email']
                            pbar.update(1)
                            await asyncio.sleep(1)
                            try:
                                auth.send_password_reset_email(email)
                                tqdm.write(f"Password reset email sent successfully to {email}")
                                last_queue = last_queue.drop(index)
                                unsent_email_queue.remove(email)
                            except Exception as error:
                                error_message = str(error)
                                if "QUOTA_EXCEEDED" in error_message:
                                    unsent_email_queue_final.append(email)
                                    if email in unsent_email_queue:
                                        unsent_email_queue.remove(email)
                                    else:
                                        pass
                                    tqdm.write(f"Email queued for unsent Emails: {email}")
                                    await asyncio.sleep(2)

                        pbar.close()

                print("Done Queued Emails sent to the inbox")
                print(f"Total Sent Email {149 - len(unsent_email_queue_final)}")
                print(f"Shutdown Auth reach last  Queue 5 left unsent emails {len(unsent_email_queue_final)}")
                shutil.rmtree(os.path.join(self.data, self.partition_name))  # Remove the entire directory

    def save_queue_data(self, queues, data, partition_name, queue_index):
        save_queue_data_frame = pd.DataFrame({"Email": queues})
        save_path = os.path.join(data, partition_name, f"queue_{queue_index}.csv")

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

        save_queue_data_frame.to_csv(save_path, index=False)
        print("Save Email recovery created successfully")


    def send_verification_email_user(self) -> None:
        """
        Send email verification requests to users liskateted in the CSV file.

        Returns:
        - None
        """
        # Read data from CSV file
        user_data = pd.read_csv(self.data_csv_path)

        # Iterate over the rows in the CSV file, sign in each user, and send email verification
        for index, row in tqdm(user_data.iterrows(), total=len(user_data), desc="Processing Sending Verification Emails"):
            email = row['Email']
            password = row['Password']

            try:
                # Sign in with email and password
                user = self.authentication.sign_in_with_email_and_password(email, password)

                # Send email verification
                self.authentication.send_email_verification(user['idToken'])
                tqdm.write(f"Email verification sent successfully to {email}")
            except Exception as e:
                tqdm.write(f"Error sending email verification to {email}: {e}")

    def change_email_address(self) -> None:
        """
        Change email addresses for users listed in the CSV file.

        Returns:
        - None
        """
        # Read data from CSV file
        user_data = pd.read_csv(self.data_csv_path)

        # Iterate over the rows in the CSV file, sign in each user, and change the email address
        for index, row in tqdm(user_data.iterrows(), total=len(user_data), desc="Processing Changing Email Addresses"):
            email = row['Email']
            password = row['Password']
            new_email = row['NewEmail']  # Assuming there's a 'NewEmail' column in the CSV

            try:
                # Sign in with current email and password
                user = self.authentication.sign_in_with_email_and_password(email, password)

                # Change email address
                self.authentication.change_email(user['idToken'], email=email)
                tqdm.write(f"Email address changed successfully for {email} to {email}")
            except Exception as e:
                tqdm.write(f"Error changing email address for {email}: {e}")


class Settings(Sender):
    def __init__(self, data_csv_path: str, authentication,config):
        super().__init__(data_csv_path, authentication,config)

    async def sending(self, method):
        if method == "reset":
            await self.send_email()
        elif method == "verify":
            self.send_verification_email_user()
        elif method == "change":
            self.change_email_address()