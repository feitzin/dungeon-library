from abc import ABC, abstractmethod

import curses
from curses import wrapper

from data import read_map

# init and cleanup
def init():
    '''
        Initializes curses.
    '''
    stdscr = curses.initscr()
    stdscr.clear()
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

class Display(ABC):
    '''
        Abstract base class for dungeon displays.
    '''
    def __init__(self):
        pass

    @abstractmethod
    def load(self, config):
        pass

    def listen(self, stdscr):
        return stdscr.getkey()

class DungeonDisplay(Display):
    '''
        Standard dungeon display class. Comes with a main map window, a bottom
        text info box, and an interactive sidebar.
    '''
    def __init__(self, config=None):
        super(DungeonDisplay, self)
        
        self.h = min(curses.LINES, 41)
        self.w = min(curses.COLS, 49)
        self.info_h = 8
        self.side_w = 16
        self.margin_h = (self.h - self.info_h)//2
        self.margin_w = (self.w - self.side_w)//2

        self.x = -1
        self.y = -1

        # Set default initialization.

        # saved world map; main map window; info/dialogue box; sidebar
        self.world = None
        self.pos = None
        self.vis = curses.newwin(self.h - self.info_h, self.w - self.side_w, 0, 0)
        self.info = curses.newwin(self.h, self.w, self.h - self.info_h, self.w - self.side_w)
        self.sidebar = curses.newwin(self.h, self.w, 0, self.w - self.side_w)

        for scr in [self.vis, self.info, self.sidebar]:
            scr.clear()
            scr.refresh()
        
        # world exploration or sidebar interaction mode
        self.mode = 'world'

        # Load specified state if given.
        if config: self.load(config)

    def load(self, config):
        '''
            Loads a config dictionary.
        '''
        # load world map
        if 'map' in config:
            self.world = read_map(config['map'])
            self.render_map()

        if 'pos' in config:
            self.move(config['pos'])

        if 'text' in config:
            self.log(config['text'])

    def render_map(self):
        '''
            Reloads world map info into the vis pad.
        '''
        h = len(self.world)
        w = len(self.world[0])
        self.vis = curses.newpad(h + 2 * self.margin_h, w + 2 * self.margin_w)

        #for i in range(h + 2 * margin_h):
        #    for j in range(w + 2 * margin_w):
        #        self.vis.addch(i, j, ' ')
        
        for i in range(h):
            for j in range(w):
                self.vis.addch(i + self.margin_h, j + self.margin_w,
                               self.world[i][j])

    def move(self, pos):
        '''
            Moves to a specified coordinate in the world map.
        '''
        if self.x != -1 and self.y != -1:
            self.vis.addch(self.x, self.y, self.world[self.x][self.y])
            
        self.x = pos[0]
        self.y = pos[1]
        self.vis.addch(self.x, self.y, '@')
        
        self.vis.refresh(max(pos[0] - self.margin_h, 0),
                         max(pos[1] - self.margin_w, 0),
                         0, 0, self.h - self.info_h, self.w - self.side_w)

    def log(self, text):
        '''
            Displays text in the infobox.
        '''
        self.info.addstr(0, 0, text)
        self.info.refresh()

    def sidebar(self, text):
        '''
            Displays text in the sidebar.
        '''
        pass

    def refresh_all(self):
        '''
            Refreshes all windows.
        '''
        if self.h != min(curses.LINES, 41) or self.w != min(curses.COLS, 49):
            self.h = min(curses.LINES, 41)
            self.w = min(curses.COLS, 49)
            self.margin_h = (self.h - self.info_h)//2
            self.margin_w = (self.w - self.side_w)//2
        pass
