import firebase
from utlis import generate_random_password, generate_gmail_email , read_file
from Config import FirebaseConfig
from Creditials import Creditials

firebase_config = FirebaseConfig(Creditials)
app = firebase_config.initialize_app()
auth = firebase_config.get_auth_instance()



if __name__ == "__main__":
    data_csv_path = 'test_data.csv'

    create_users_in_firebase(data_csv_path)
    send_password_reset_email(data_csv_path)
    
