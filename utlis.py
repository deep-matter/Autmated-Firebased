import pandas as pd
from typing import Dict
import random
import string
import csv


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def separate_data(file_path):
    list_emails = []

    with open(file_path, "r") as file:
        for line in file:
            list_emails.append(line.strip())

    max_length = 1
    partition_index = 0
    data_split = {"Email": [], "password": []}
    after_test_email = "Badreddinebouzourhoun@gmail.com"

    for email in list_emails:
        password = generate_random_password()

        data_split["Email"].append(email)
        data_split["password"].append(password)

        if len(data_split["Email"]) % max_length == 0:
            partition_index += 1
            # Append after_test_email to each partition
            data_split["Email"].append(after_test_email)
            data_split["password"].append(password)
            
            partition_data = pd.DataFrame(data_split)
            partition_data.to_csv(f"Data/test_data_{partition_index}.csv", index=False)
            data_split = {"Email": [], "password": []}

    # Save the remaining data if any
    if data_split["Email"]:
        partition_index += 1
        partition_data = pd.DataFrame(data_split)
        partition_data.to_csv(f"Data/test_data_{partition_index}.csv", index=False)



def generate_gmail_email(real_name):
    first_name = real_name.split()[0].lower()
    random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"{first_name}@gmail.com"



def TXT_to_CSV(FILE_TXT):
    """
    Task: Read a text file line by line and convert it to a CSV file with columns [Email, Password].

    Args:
    - FILE_TXT (str): Path to the input text file.

    Returns:
    - None
    """
    # Ensure the file has the correct extension
    if not FILE_TXT.endswith('.txt'):
        print("Error: Input file must be a text file (.txt)")
        return

    # Open the text file for reading
    with open(FILE_TXT, 'r') as txt_file:
        # Read lines from the text file
        lines = txt_file.readlines()

    # Extract emails and passwords from the lines (modify this part based on your text file structure)
    data = []
    for line in lines:
        # Assuming each line has email and password separated by a space
        email, password = line.strip().split(' ')
        data.append([email, password])

    # Write the data to a CSV file
    csv_file_path = FILE_TXT.replace('.txt', '_output.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        # Define CSV writer
        csv_writer = csv.writer(csv_file)

        # Write header
        csv_writer.writerow(['Email', 'Password'])

        # Write data rows
        csv_writer.writerows(data)

    print(f"Conversion completed. CSV file saved at: {csv_file_path}")



def read_file(data_csv: str) -> Dict[str, str]:
    """
    Args:
    - data_csv (str): Path to the CSV file.

    Returns:
    - user_password_dict (Dict[str, str]): Dictionary containing user and password pairs.
    """
    try:
        # Read CSV file into a DataFrame
        data = pd.read_csv(data_csv)

        # Create an empty dictionary to store user and password pairs
        user_password_dict = {}

        # Iterate over the rows of the DataFrame
        for index, row in data.iterrows():
            # Assuming the CSV file has columns named 'user' and 'password'
            user = row['Email']
            password = row['Password']

            # Store user and password in the dictionary
            user_password_dict[user] = password

            # Print user and password (you can customize this part as needed)
            print(f"Email: {user}, Password: {password}")

        return user_password_dict

    except Exception as e:
        print(f"Error: {e}")
        return {}

# if __name__ == "__main__":
#    # Sample data for testing
#     num_users = 5
#     real_names = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown']

#     # Create a DataFrame
#     data = {
#         'Email': [generate_gmail_email(name) for name in real_names],
#         'Password': [generate_random_password() for _ in range(num_users)]
#     }

#     test_dataframe = pd.DataFrame(data)

#     test_dataframe.to_csv('test_data.csv', index=False)

    
#     csv_file_path = 'test_data.csv'
#     user_password_data = read_file(csv_file_path)



