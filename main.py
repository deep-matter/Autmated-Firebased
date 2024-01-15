import firebase
from utlis import generate_random_password, generate_gmail_email, read_file
from Config import FirebaseConfig
from Creditials import Creditials
from core.Sender import Sender , Settings
from core.Manager import *
import os 
from utlis import separate_data
from Screen import Screen_log
import time
import asyncio
from parser import *

def Clear():
    os.system("clear")
    Screen_log()
    time.sleep(1)

def Inputs_Create():
    DATA = input("Add the path DATA emails:")
    return DATA

def Inputs_Split():
    DATA = input("Add the path DATA emails to split:")
    return DATA

def Inputs_Send():
    DATA = input("Add the path DATA emails:")
    METHOD = input("Set the Method Sending:")
    return DATA, METHOD

async def main():
    try:
        Clear()
        print("1: Insert the Data into Firebase Users")
        print("2: Send Email with Reset Password Method to set reset")
        print("3: Split that Email into sub-Files")
        print("99: Exiting from tool Press CTRL + C")
        Choices = input("\n Please insert the choice: ")

        if Choices == "1":
            Clear()
            DATA = Inputs_Create()
            create_users_in_firebase(DATA, auth=auth)
            print("Wait Please, the tool will automatically reload.")
            await asyncio.sleep(8)
            return main()

        elif Choices == "2":
            Clear()
            DATA, METHOD = Inputs_Send()
             #Create an instance of the Settings class
            settings_Sender = Settings(data_csv_path=DATA, authentication=auth)
            await settings_Sender.sending(method=METHOD)
            print("Wait Please, the tool will automatically reload.")
            await asyncio.sleep(8)

        elif Choices == "3":
            Clear()
            DATA = Inputs_Split()
            separate_data(DATA)
            print("done splitation.")
            print("Wait Please, the tool will automatically reload.")
            await asyncio.sleep(8)
            return main()

        elif Choices == "99":
            Clear()
            print(f" For more information of each API follwoing :\n")
            print("Creating Data users be sure to have the right path of Data")
            print("to send with Reset Password be Sure to Set the method to reset")
            print("Exiting from the tool. Press CTRL + C to exit.")
            await asyncio.sleep(8)
            return
        else:
            print("You inserted an invalid option. The tool will reload automatically. Please wait...")
            await asyncio.sleep(8)
            return main()
    except KeyboardInterrupt:
        print("\nExiting from the tool. Press CTRL + C to exit.")
        await asyncio.sleep(8)
        return

if __name__ == "__main__":
    main()
