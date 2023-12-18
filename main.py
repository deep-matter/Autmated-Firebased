import firebase
from utlis import generate_random_password, generate_gmail_email, read_file
from Config import FirebaseConfig
from Creditials import Creditials
from core.Sender import Sender
from core.Manager import *
import os 
from Screen import Screen_log
import time

def Clear():
    os.system("clear")
    Screen_log()
    time.sleep(1)

def Inputs_Create():
    DATA = input("Add the path DATA emails:")
    return DATA

def Inputs_Send():
    DATA = input("Add the path DATA emails:")
    METHOD = input("Set the Method Sending:")
    return DATA, METHOD

def main():
    try:
        firebase_config = FirebaseConfig(Creditials)
        app = firebase_config.initialize_app()
        auth = firebase_config.get_auth_instance()
        Clear()
        print("1: Insert the Data into Firebase Users")
        print("2: Send Email with Reset Password Method to set reset")
        print("99: Exiting from tool Press CTRL + C")
        Choices = input("\n Please insert the choice: ")

        if Choices == "1":
            Clear()
            DATA = Inputs_Create()
            create_users_in_firebase(DATA, auth=auth)
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()
        elif Choices == "2":
            Clear()
            DATA, METHOD = Inputs_Send()
            Sender(data_csv_path=DATA, authentication=auth, method=METHOD).send_password_reset_email()
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()
        elif Choices == "99":
            Clear()
            print(f" For more information of each API follwoing :\n")
            print("Creating Data users be sure to have the right path of Data")
            print("to send with Reset Password be Sure to Set the method to reset")
            print("Exiting from the tool. Press CTRL + C to exit.")
            time.sleep(3)
            return
        else:
            print("You inserted an invalid option. The tool will reload automatically. Please wait...")
            time.sleep(8)
            return main()
    except KeyboardInterrupt:
        print("\nExiting from the tool. Press CTRL + C to exit.")
        time.sleep(3)
        return

if __name__ == "__main__":
    main()
