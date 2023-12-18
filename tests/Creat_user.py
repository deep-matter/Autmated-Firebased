import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from firebase import firebase
import pandas as pd
from tqdm import tqdm

config = {
    "apiKey": "AIzaSyDtQPBX8qQZ22xyNCaAANg02XDM_bfN0uk",
    "authDomain": "add-user-e98e9.firebaseapp.com",
    "projectId": "add-user-e98e9",
    "storageBucket": "add-user-e98e9.appspot.com",
    "messagingSenderId": "858288259676",
    "appId": "1:858288259676:web:52354ec6f2a90f13581c99",
    "measurementId": "G-D0WPTFDN0K"
}

firebase.initialize_app(config)

auth = firebase.auth()

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

# Unit test for create_users_in_firebase function
class TestCreateUsersFunction(unittest.TestCase):
    def test_create_users(self):
        data_csv = 'path/to/your/test_data.csv'
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            create_users_in_firebase(data_csv)

        output = mock_stdout.getvalue()
        self.assertIn("Creating users", output)
        self.assertIn("User created successfully", output)

if __name__ == "__main__":
    unittest.main()
