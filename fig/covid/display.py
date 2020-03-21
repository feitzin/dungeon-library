import curses
from curses import wrapper

from time import sleep

import sys
sys.path.append('../dungeon')

from dungeon import Dungeon
from graphics import DungeonDisplay
from data import load

def main(stdscr):
    stdscr.clear()
    display = DungeonDisplay(stdscr, load('resources/config/start.config'))
    sleep(3)

wrapper(main)
