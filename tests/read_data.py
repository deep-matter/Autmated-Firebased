import unittest
import pandas as pd
import os

def generate_random_password(length: int = 8) -> str:
    """Generate a random password.

    Args:
    - length (int): The length of the generated password.

    Returns:
    - str: The randomly generated password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_gmail_email(real_name: str) -> str:
    """Generate a Gmail-like email address using a real name.

    Args:
    - real_name (str): The real name to be used in the email address.

    Returns:
    - str: The generated Gmail-like email address.
    """
    first_name = real_name.split()[0].lower()
    random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"{first_name}@gmail.com"

def txt_to_csv(file_txt: str) -> None:
    """Read a text file line by line and convert it to a CSV file with columns [Email, Password].

    Args:
    - file_txt (str): Path to the input text file.

    Returns:
    - None
    """
    if not file_txt.endswith('.txt'):
        print("Error: Input file must be a text file (.txt)")
        return

    with open(file_txt, 'r') as txt_file:
        lines = txt_file.readlines()

    data = [[line.split()[0], line.split()[1]] for line in lines]

    csv_file_path = file_txt.replace('.txt', '_output.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Email', 'Password'])
        csv_writer.writerows(data)

    print(f"Conversion completed. CSV file saved at: {csv_file_path}")

def read_csv_file(data_csv: str) -> Dict[str, str]:
    """Read a CSV file and return a dictionary containing user and password pairs.

    Args:
    - data_csv (str): Path to the CSV file.

    Returns:
    - user_password_dict (Dict[str, str]): Dictionary containing user and password pairs.
    """
    try:
        data = pd.read_csv(data_csv)
        user_password_dict = {}

        for index, row in data.iterrows():
            user = row['Email']
            password = row['Password']
            user_password_dict[user] = password

        return user_password_dict

    except Exception as e:
        print(f"Error: {e}")
        return {}

class TestAuthFunctions(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_dir'
        os.makedirs(self.test_dir, exist_ok=True)

        self.num_users = 5
        self.real_names = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown']

        self.data = {
            'Email': [generate_gmail_email(name) for name in self.real_names],
            'Password': [generate_random_password() for _ in range(self.num_users)]
        }

        self.test_dataframe = pd.DataFrame(self.data)

    def tearDown(self):
        os.rmdir(self.test_dir)

    def test_txt_to_csv_conversion(self):
        test_file_path = os.path.join(self.test_dir, 'test_data.txt')
        self.test_dataframe.to_csv(test_file_path, sep=' ', index=False, header=False)
        txt_to_csv(test_file_path)
        csv_file_path = os.path.join(self.test_dir, 'test_data_output.csv')
        self.assertTrue(os.path.exists(csv_file_path))
        result_dataframe = pd.read_csv(csv_file_path)
        self.assertTrue(result_dataframe.equals(self.test_dataframe))

    def test_read_csv_file(self):
        csv_file_path = os.path.join(self.test_dir, 'test_data.csv')
        self.test_dataframe.to_csv(csv_file_path, index=False)
        user_password_data = read_csv_file(csv_file_path)
        expected_data = dict(zip(self.test_dataframe['Email'], self.test_dataframe['Password']))
        self.assertDictEqual(user_password_data, expected_data)

if __name__ == '__main__':
    unittest.main()
