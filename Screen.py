from termcolor import colored
import sys  
import random
import time
import os 

def Screen_log():
    color_logo = ['red', 'green', 'yellow']
    random_color = random.choice(color_logo)
    print(colored(
    """
 _______    ______   __    __   ______   ________  ______ 
|       \  /      \ |  \  |  \ /      \ |        \|      \\
| $$$$$$$\|  $$$$$$\| $$  | $$|  $$$$$$\| $$$$$$$$ \$$$$$$
| $$  | $$| $$  | $$| $$  | $$| $$__| $$| $$__      | $$  
| $$  | $$| $$  | $$| $$  | $$| $$    $$| $$  \     | $$  
| $$  | $$| $$  | $$| $$  | $$| $$$$$$$$| $$$$$     | $$  
| $$__/ $$| $$__/ $$| $$__/ $$| $$  | $$| $$_____  _| $$_ 
| $$    $$ \$$    $$ \$$    $$| $$  | $$| $$     \|   $$ \\
 \$$$$$$$   \$$$$$$   \$$$$$$  \$$   \$$ \$$$$$$$$ \$$$$$$
                                                          
                                                          
Created by Deep-Matter i am sorry DOUAE really i am if i didn't do that will not make this tool""",
random_color))
    time.sleep(1)


if __name__ == "__main__":
    Screen_log()