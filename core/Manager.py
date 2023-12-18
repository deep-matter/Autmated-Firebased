import pandas as pd
from tqdm import tqdm

def create_users_in_firebase(data_csv,auth):
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
