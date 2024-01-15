import curses
import random
import time

class AnimatedLogoPrinter:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.color_logo = ['red', 'green', 'yellow']
        self.random_color = self.getRandomColor()
        self.init_curses()
        self.animate_logo()

    def init_curses(self):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def printAnimatedLogo(self):
        self.stdscr.addstr(
            0, 0,
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
            curses.color_pair(self.color_logo.index(self.random_color) + 1)
        )

    def getRandomColor(self):
        return random.choice(self.color_logo)

    def animate_logo(self):
        for _ in range(3):  # Adjust the number of animation iterations as needed
            self.stdscr.clear()
            self.printAnimatedLogo()
            self.stdscr.refresh()
            time.sleep(1)

def main(stdscr):
    animated_logo = AnimatedLogoPrinter(stdscr)
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)