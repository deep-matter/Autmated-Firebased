from typing import Optional
from numpy import ndarray
import pandas as pd
from tqdm import tqdm
import time

from typing import Optional
import pandas as pd
from tqdm import tqdm
import time

class Sender:
    def __init__(self, data_csv_path: str, authentication):
        self.data_csv_path = data_csv_path
        self.authentication = authentication
        self.queues = [[] for _ in range(5)]

    def send_password_reset_email(self) -> None:
        """
        Send password reset emails to users listed in the CSV file.

        Returns:
        - None
        """
        # Read data from CSV file
        user_data = pd.read_csv(self.data_csv_path)

        # Iterate over the rows in the CSV file and send password reset emails
        for index, row in tqdm(user_data.iterrows(), total=len(user_data), desc="Processing Sending Password Reset Emails"):
            email = row['Email']
            time.sleep(1)
            try:
                # Send password reset email
                self.authentication.send_password_reset_email(email)
                tqdm.write(f"Password reset email sent successfully to {email}")

            except Exception as e:
                # Handle the error if the email quota is exceeded
                error_message = str(e)
                if "QUOTA_EXCEEDED" in error_message:
                    self.queues[0].append(email)
                    tqdm.write(f"Email queued for sending later: {email}")
                    time.sleep(2)

        self.process_queued_emails()

    def process_queued_emails(self) -> None:
        for i, queue in enumerate(self.queues):
            if queue:
                tqdm.write(f"Start Queued {i+1} Emails left in the database to be sent")
                for email in queue:
                    try:
                        self.authentication.send_password_reset_email(email)
                        tqdm.write(f"Password reset email sent successfully from queue to {email}")
                    except Exception as e:
                        error_message = str(e)
                        if "QUOTA_EXCEEDED" in error_message:
                            self.queues[(i+1) % 5].append(email)
                            tqdm.write(f"Email queued for sending later: {email}")
                            time.sleep(2)
                time.sleep(1)
                tqdm.write(f"Freze Queue {i+2} the Auth for Period of time")
                time.sleep(1)
                
        print(f"Done Queued Emails sent to the database")

    def send_verification_email_user(self) -> None:
        """
        Send email verification requests to users listed in the CSV file.

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
    def __init__(self, data_csv_path: str, authentication):
        super().__init__(data_csv_path, authentication)

    def sending(self, method):
        if method == "reset":
            self.send_password_reset_email()
        elif method == "verify":
            self.send_verification_email_user()
        elif method == "change":
            self.change_email_address()