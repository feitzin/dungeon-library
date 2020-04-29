import curses
from curses import wrapper

import sys
sys.path.append('../dungeon')

from dungeon import Dungeon
from graphics import DungeonDisplay
from data import load

def main(stdscr):
    config = load('resources/config/start.config')
    
    display = DungeonDisplay(stdscr, config=config)
    dungeon = Dungeon(display=display, config=config)

    curses.curs_set(0)

    directions = {
        "KEY_LEFT": dungeon.LEFT,
        "KEY_RIGHT": dungeon.RIGHT,
        "KEY_UP": dungeon.UP,
        "KEY_DOWN": dungeon.DOWN
    }
    
    while True:
        key = stdscr.getkey()
        #display.log('key received')
        if key in directions:
            display.log('')
            dungeon.move(directions[key])
        else:
            if key == ' ':
                dungeon.act()
            elif key == 'l':
                dungeon.look()
        
if __name__ == "__main__":
    wrapper(main)
