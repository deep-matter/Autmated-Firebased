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
            
              888.                                              
            .8"888.      .oooooooo  .ooooo.  oooo d8b  .oooo.   
           .8' `888.    888' `88b  d88' `88b `888""8P `P  )88b  
          .88ooo8888.   888   888  888   888  888      .oP"888  
         .8'     `888.  `88bod8P'  888   888  888     d8(  888  
        o88o     o8888o `8oooooo.  `Y8bod8P' d888b    `Y888""8o 
                        d"     YD                               
                        "Y88888P'                               
            
                                                                  
        Created by Deep-Matter for 365 days per FIRE SEND """,
random_color))
    time.sleep(1)


if __name__ == "__main__":
    Screen_log()