import firebase
import pandas as pd
import string
import random
from tqdm import tqdm
from utlis import generate_random_password, generate_gmail_email , read_file
from Config import FirebaseConfig
from Creditials import Creditials

firebase_config = FirebaseConfig(Creditials)
firebase_config.initialize_app()
auth = firebase_config.get_auth_instance()

def create_users_in_firebase(data_csv):
    """
    Create users in Firebase from a CSV file.

    Args:
    - data_csv (str): Path to the CSV file containing user data.

    Returns:
    - None
    """
    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Use tqdm for better progress visualization
    for _, row in tqdm(user_data.iterrows(), total=len(user_data), desc="Creating users"):
        email = row['Email']
        password = row['Password']

        # Create a new user
        try:
            auth.create_user_with_email_and_password(email, password)
            tqdm.write(f"User created successfully for email: {email}")
        except Exception as e:
            # Handle the error if the email already exists
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                tqdm.write(f"Email {email} already exists.")
            else:
                tqdm.write(f"Error creating user for email {email}: {error_message}")



def send_password_reset_email(data_csv):
    """
    Send password reset emails to users listed in the CSV file.

    Args:
    - data_csv (str): Path to the CSV file containing user data.

    Returns:
    - None
    """
    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Iterate over the rows in the CSV file and send password reset emails
    for index, row in user_data.iterrows():
        email = row['Email']

        try:
            # Send password reset email
            auth.send_password_reset_email(email)
            print(f"Password reset email sent successfully to {email}")
        except Exception as e:
            print(f"Error sending password reset email to {email}: {e}")


def send_verification_email_user(data_csv):
    """
    Send email verification requests to users listed in the CSV file.

    Args:
    - data_csv (str): Path to the CSV file containing user data.

    Returns:
    - None
    """
    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Iterate over the rows in the CSV file, sign in each user, and send email verification
    for index, row in user_data.iterrows():
        email = row['Email']
        password = row['Password']

        try:
            # Sign in with email and password
            user = auth.sign_in_with_email_and_password(email, password)

            # Send email verification
            auth.send_email_verification(user['idToken'])
            print(f"Email verification sent successfully to {email}")
        except Exception as e:
            print(f"Error sending email verification to {email}: {e}")


def change_email_address(data_csv):
    """
    Change email addresses for users listed in the CSV file.

    Args:
    - data_csv (str): Path to the CSV file containing user data.

    Returns:
    - None
    """
    # Read data from CSV file
    user_data = pd.read_csv(data_csv)

    # Iterate over the rows in the CSV file, sign in each user, and change the email address
    for index, row in user_data.iterrows():
        email = row['Email']
        password = row['Password']
        new_email = row['NewEmail']  # Assuming there's a 'NewEmail' column in the CSV

        try:
            # Sign in with current email and password
            user = auth.sign_in_with_email_and_password(email, password)

            # Change email address
            auth.change_email(user['idToken'], email=new_email)
            print(f"Email address changed successfully for {email} to {new_email}")
        except Exception as e:
            print(f"Error changing email address for {email}: {e}")


def delete_email_address(data_csv, email_filters):
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


def remove_database_user(data_csv, email_filters=None):
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
    users = db.child('users').get('Email')
    print(users)

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


def retrieve_database_user_filter(data_csv, email_filters=None):
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

    # Retrieve users from the database
    users = db.child('users').get()
    print(users)

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


if __name__ == "__main__":
    # Specify the path to the test data CSV file
    data_csv_path = 'test_data.csv'

    # Call the function to create users in Firebase
    create_users_in_firebase(data_csv_path)
    ##ethod Seneing 1 - Firebase
    #send_password_reset_email(data_csv_path)
    ##ethod Seneing 2 - Firebase
    #send_verification_email_user(data_csv_path)
    ##ethod Seneing 3 - Firebase
    #change_email_address(data_csv_path)


    ##### MAnganing the database User  Firebase Authentication ######
    # Specify the email filters
    email_filters = ["gmail.com", "yahoo.com", "outlook.com"]

    
     # Call the function to retrieve and print database users based on filters
    #retrieved_emails_dict = retrieve_database_user_filter(data_csv_path, email_filters)

    # Do something with the retrieved emails if needed
    #print("Retrieved emails:", retrieved_emails_dict)
    # Call the function to delete user accounts based on filters
    #delete_email_address(data_csv_path, email_filters)
    # Call the function to remove database users based on filters
    #remove_database_user(data_csv_path, email_filters)
