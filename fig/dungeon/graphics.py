from abc import ABC, abstractmethod

import curses
from curses import wrapper

# init and cleanup
def init():
    '''
        Initializes curses.
    '''
    curses.noecho()
    curses.cbreak()

def end(windows):
    '''
        Cleans up and returns to previous state.
    '''
    curses.nocbreak()
    for scr in windows:
        scr.keypad(False)
    curses.echo()
    curses.endwin()

# curses wrapper
def run(driver):
    wrapper(driver)

class Display(ABC):
    '''
        Abstract base class for dungeon displays.
    '''
    def __init__(self):
        pass

    @abstractmethod
    def save(self, config):
        pass

    @abstractmethod
    def load(self, config):
        pass

    @abstractmethod
    def run(self):
        pass

class DungeonDisplay(Display):
    '''
        Standard dungeon display class. Comes with a main map window, a bottom
        text info box, and an interactive sidebar.
    '''
    def __init__(self, config=None):
        height = curses.LINES
        width = curses.COLS
        
        #self.vis = curses.newwin(height - 8, width - 16, 0, 0) # main map window
        self.vis = None
        self.info = curses.newwin(height, width, height - 8, width - 16) # info box
        self.sidebar = curses.newwin(height, width, 0, width - 16) # sidebar

        if config: load(config)

        if self.vis is not None: self.vis.keypad = True
        self.sidebar.keypad=True

    def load(config):
        pass

    def save(self, config):
        pass

    def run(self):
        pass
