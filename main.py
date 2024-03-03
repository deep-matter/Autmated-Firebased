import os 
import sys
current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, target_dir)

from Helper.utlis import *
from Helper.parser import *
import os 
from Helper.Screen import Screen_log
import time
import asyncio
import curses
from paralle.worker_email import worker_emails , process_apps_emails
from paralle.worker_sender_ascyn import worker_senders , process_apps_Sender

def Clear():
    os.system("clear")
    Screen_log()
    time.sleep(1)

def Inputs_Create():
    DATA = input("Add the path DATA emails: ")
    return DATA

def Inputs_Split():
    DATA = input("Add the path DATA emails to split: ")
    return DATA

def Inputs_Parser():
    DATA = input("Add the path Config projects to parese: ")
    return DATA

def Inputs_Send():
    DATA = input("Add the path DATA emails: ")
    METHOD = input("Set the Method Sending: ")
    return DATA, METHOD

def main():
    apps_path = "apps/"  # Replace with your actual path
    data_path = "Data/"  # Replace with your actual path
    try:
        Clear()
        print("1: Insert the Data into Firebase Users")
        print("2: Send Email with Reset Password Method to set reset")
        print("3: Split that Email into sub-Files")
        print("4: Config Senders Creditionals")

        print("99: Exiting from tool Press CTRL + C")
        Choices = input("\n Please insert the choice: ")

        if Choices == "1":
            Clear()
            
            loop = asyncio.get_event_loop()

            loop.run_until_complete(process_apps_emails(worker_emails, data_path, apps_path))
            
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()

        elif Choices == "2":
            Clear()

            loop = asyncio.get_event_loop()

            loop.run_until_complete(process_apps_Sender(worker_senders, data_path, apps_path))
            
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()

       
        elif Choices == "3":
            Clear()
            DATA = Inputs_Split()
            separate_data(DATA)
            print("done splitation.")
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()

        elif Choices == "4":
            Clear()
            DATA = Inputs_Parser()
            print(DATA)
            parse(DATA)
            print("Config Createed .")
            print("Wait Please, the tool will automatically reload.")
            time.sleep(8)
            return main()

        elif Choices == "99":
            Clear()
            print(f" For more information of each API follwoing :\n")
            print("Creating Data users be sure to have the right path of Data")
            print("to send with Reset Password be Sure to Set the method to reset")
            print("Exiting from the tool. Press CTRL + C to exit.")
            time.sleep(8)
            return
        else:
            print("You inserted an invalid option. The tool will reload automatically. Please wait...")
            time.sleep(8)
            return  main()
    except KeyboardInterrupt:
        print("\nExiting from the tool. Press CTRL + C to exit.")
        time.sleep(8)
        return

if __name__ == "__main__":
    main()
