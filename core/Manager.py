import pandas as pd
from tqdm import tqdm
import asyncio
from utlis import re_initialized_auth
import os

queue_email = []
queue_pass = []

def save_queue_data(self, queues, data, partition_name, queue_index):
        save_queue_data_frame = pd.DataFrame({"Email": queues[queue_index]})
        save_path = os.path.join(data, partition_name, f"queue_{queue_index}.csv")

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

        save_queue_data_frame.to_csv(save_path, index=False)
        print("Save Email recovery created successfully")

def split_data(data_csv, n_splits):
    """
    Split data into n_splits chunks and save each part to a separate CSV file.
    """
    partition_name = os.path.splitext(os.path.basename(data_csv))[0]
    data_df = pd.read_csv(data_csv)
    data = "./Data/"
    # Calculate the size of each chunk
    print(len(data_df))
    chunk_size = len(data_df) // n_splits
    save_path = data + partition_name
    if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)
# In    

    # Iterate over the number of splits
    for i in range(n_splits):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < n_splits - 1 else len(data_df)
    
        # Extract the data for the current chunk
        data_part = data_df[start_index:end_index]

        data_part.to_csv(os.path.join(save_path,f"part_{i + 1}.csv"), index=False)


async def Push_Emails(data_part , auth , index_parition , config):
    if index_parition > 1:
        await asyncio.sleep(2)
        re_auth = re_initialized_auth(config)
        with tqdm(total=len(data_part), desc=f"Creating users partiton {index_parition}") as pbar:
            for _, row in data_part.iterrows():
                pbar.update(1)
                email = row['Email']
                password = row['Password']
                await asyncio.sleep(2)
                # Create a new user
                try:
                    re_auth.create_user_with_email_and_password(email, password)
                    tqdm.write(f"User created successfully for email: {email}")
                except Exception as e:
                    # Handle the error if the email already exists
                    error_message = str(e)
                    if "EMAIL_EXISTS" in error_message:
                        tqdm.write(f"Email {email} already exists.")

                    if "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                        queue_email.append(email)
                        queue_pass.append(password)
                        tqdm.write(f"Email queued for creating later: {email}")
                        await asyncio.sleep(2)
                    else:
                        tqdm.write(f"done creating user for emails from partition {index_parition}")
        

            pbar.close()
    else :
        with tqdm(total=len(data_part), desc=f"Creating users partiton {index_parition}") as pbar:
            for _, row in data_part.iterrows():
                pbar.update(1)
                email = row['Email']
                password = row['Password']
                await asyncio.sleep(2)
                # Create a new user
                try:
                    auth.create_user_with_email_and_password(email, password)
                    tqdm.write(f"User created successfully for email: {email}")
                except Exception as e:
                    # Handle the error if the email already exists
                    error_message = str(e)
                    if "EMAIL_EXISTS" in error_message:
                        tqdm.write(f"Email {email} already exists.")

                    if "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                        queue_email.append(email)
                        queue_pass.append(password)
                        tqdm.write(f"Email queued for creating later: {email}")
                        await asyncio.sleep(2)
                    else:
                        tqdm.write(f"done creating user for emails from partition {index_parition}")
        
            pbar.close()
        
        

async def create_users_in_firebase(data_csv, auth, config):
    """
    Create users in Firebase from a CSV file.

    Args:
    - data_csv (str): Path to the CSV file containing user data.

    Returns:
    - None
    """
    # Read data from CSV file
    
    #user_data = pd.read_csv(data_csv)
    print(data_csv)
    split_data(data_csv, 3)
    exit()

    partition_name = os.path.splitext(os.path.basename(data_csv))[0]
    data = "./Data/"
    path = data + partition_name
    print(path)
    for partition in range(1, 4):
        data_part = pd.read_csv(f"{path}/part_{partition}.csv")
        await Push_Emails(data_part, auth, partition, config)
        await asyncio.sleep(3)




def delete_email_address(data_csv, email_filters, auth):
    """
    Delete user accounts based on email filters.

    Args:
    - data_csv (str): Path to the CSV file containing user data.
    - email_filters (list): List of email domains to filter users.

    Returns:
    - None
    """
    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Iterate over the rows in the CSV file, sign in each user, and delete user accounts based on filters
    for index, row in user_data.iterrows():
        email = row['Email']

        # Check if the email matches any of the filters
        if any(filter in email for filter in email_filters):
            try:
                # Sign in with email and password
                user = auth.sign_in_with_email_and_password(email, row['Password'])

                # Delete the user account
                auth.delete_user_account(user['idToken'])
                print(f"User account deleted successfully for {email}")
            except Exception as e:
                print(f"Error deleting user account for {email}: {e}")


def remove_database_user(data_csv, app,email_filters=None):
    """
    Remove database users based on email filters.

    Args:
    - data_csv (str): Path to the CSV file containing user data.
    - email_filters (list): List of email domains to filter users.

    Returns:
    - None
    """
    if email_filters is None:
        email_filters = []

    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Retrieve users from the database
    # Firebase Realtime Database
    db = app.database()
    users = db.child('users').get('Email')

    # Iterate over the retrieved users and filter based on email domains
    for user in users.each():
        user_data = user.val()

        # Check if the user's email matches any of the filters
        if any(filter in user_data['email'] for filter in email_filters):
            try:
                # Remove the user from the database
                db.child('users').child(user.key()).remove()
                print(f"User removed successfully for email: {user_data['email']}")
            except Exception as e:
                print(f"Error removing user for email {user_data['email']}: {e}")


def retrieve_database_user_filter(data_csv,app,email_filters=None):
    """
    Retrieve database users based on email filters.

    Args:
    - data_csv (str): Path to the CSV file containing user data.
    - email_filters (list): List of email domains to filter users.

    Returns:
    - Dict: Each filter corresponds to a list of filtered emails.
    """
    if email_filters is None:
        email_filters = []

    # Read data from CSV file
    user_data = pd.read_csv(data_csv)
    # Firebase Realtime Database
    db = app.database()

    users = db.child('users').get()

    # Initialize the dictionary to store filtered emails
    filtered_emails_dict = {filter: [] for filter in email_filters}

    # Iterate over the retrieved users and filter based on email domains
    for user in users.each():
        user_data = user.val()

        # Check if the user's email matches any of the filters
        for filter in email_filters:
            if user_data['email'].endswith(filter):
                email = user_data['email']
                filtered_emails_dict[filter].append(email)
                print(email)

    return filtered_emails_dict
