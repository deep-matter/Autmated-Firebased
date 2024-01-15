from typing import Optional
from numpy import exceptions
import pandas as pd
from tqdm import tqdm
import asyncio
from utlis import re_intialized_auth  # Make sure to import the required module

class Sender:
    def __init__(self, data_csv_path: str, authentication, config):
        self.data_csv_path = data_csv_path
        self.authentication = authentication
        self.queues = [[] for _ in range(5)]  # Initializing five queues
        self.config = config

    async def re_auth(self, queue_index):
        auth = re_intialized_auth(self.config)
        if queue_index == 0:
            pass
        else:
            return await self.process_queued_emails(queue_index=queue_index, auth=auth)

    async def send_email(self, email) -> None:
        user_data = pd.read_csv(self.data_csv_path)
        for queue_index in range(5):
            if queue_index == 0 :
                for index, row in tqdm(user_data.iterrows(), total=len(user_data), desc="Processing Sending Password Reset Emails"):
                    email_csv = row['Email']
                    await asyncio.sleep(1)
                    try:
                            self.authentication.send_password_reset_email(email_csv)
                            tqdm.write(f"Password reset email sent successfully to {email}")
                            await asyncio.sleep(1)
                            if self.queues[queue_index] is not None:
                                self.queues[queue_index].remove(email)
                                await asyncio.sleep(0.5)
                            user_data = user_data.drop(index)

                    except Exception as send_error:  # Replace EmailSendError with the actual exception you are expecting
                        error_message = str(send_error)
                        if "QUOTA_EXCEEDED" in error_message:
                            self.queues[queue_index].append(email)
                            tqdm.write(f"Email queued for sending later (Queue {queue_index}): {email}")
                            await asyncio.sleep(2)
                            
            await self.re_auth(queue_index=queue_index)

    async def process_queued_emails(self, queue_index, auth) -> None:
        queue = self.queues[queue_index - 1]
        if len(queue) > 0:
            tqdm.write(f"Start Queued Emails in Queue {queue_index - 1} left in the database to be sent")
            try:
                for email in queue:
                    auth.send_password_reset_email(email) 
                    tqdm.write(f"Password reset email sent successfully to {email}")
                    await asyncio.sleep(1)
                    if self.queues[queue_index] is not None:
                        self.queues[queue_index].remove(email)
                        await asyncio.sleep(0.5)   
                        
            except Exception as error:  # Replace EmailSendError with the actual exception you are expecting
                    error_message = str(error)
                    if "QUOTA_EXCEEDED" in error_message:
                        self.queues[queue_index].append(email)
                        tqdm.write(f"Email queued for sending later (Queue {queue_index}): {email}")
                        await asyncio.sleep(2)

            tqdm.write(f"Freeze Queue {queue_index - 1} the Auth for a period of time")
            await asyncio.sleep(1)

        while any(len(queue) > 0 for queue in self.queues):
            for i, queue in enumerate(self.queues):
                if len(queue) > 0:
                    tqdm.write(f"Continue processing Queue {i - 1}")
                    tasks = [self.send_email(email) for email in queue]
                    await asyncio.gather(*tasks)
                    tqdm.write(f"Freeze Queue {i - 1} the Auth for a period of time")
                    await asyncio.sleep(1)

        print("Done Queued Emails sent to the inbox")