from abc import ABC, abstractmethod

import curses
from curses import wrapper

from data import read_map, read_icon, read_key

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

def get_style(style):
    '''
        Converts from string to curses style attribute.
    '''
    s = style.lower()
    if s == 'blink':
        return curses.A_BLINK
    if s == 'bold':
        return curses.A_BOLD
    if s == 'dim':
        return curses.A_DIM
    if s == 'reverse':
        return curses.A_REVERSE
    if s == 'standout':
        return curses.A_STANDOUT
    if s == 'underline':
        return curses.A_UNDERLINE
    return None
    
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
    def __init__(self, stdscr, config=None):
        super(DungeonDisplay, self)

        # constants
        self.MAX_HEIGHT = 51
        self.MAX_WIDTH = 128
        
        self.info_h = 8
        self.side_w = 24

        # initialize sizes
        self.h = min(curses.LINES, self.MAX_HEIGHT)
        self.w = min(curses.COLS, self.MAX_WIDTH)
        self.margin_h = (self.h - self.info_h - 2)//2
        self.margin_w = (self.w - self.side_w - 1)//2
        self.vh = 2 * self.margin_h + 1
        self.vw = 2 * self.margin_w + 1

        # color settings
        self.palette = None
        self.colors = None
        self.styles = None

        self.x = -1
        self.y = -1

        # Set default initialization.

        # saved world map; main map window; info/dialogue box; sidebar
        self.world = None
        self.pos = None
        self.text = None
        self.sidetext = None
        self.icon = None
        self.key = None
        
        self.scr = stdscr

        # Load specified state if given.
        self.refresh()
        if config: self.load(config)

    def load(self, config):
        '''
            Loads a config dictionary.
        '''
        if 'rendering' in config:
            self.key = read_key(config['rendering'])

        if 'map' in config:
            self.world = read_map(config['map'])
            self.x = -1
            self.y = -1
            self.render_map()

        if 'pos' in config:
            self.move(config['pos'])

        if 'text' in config:
            self.text = config['text']
            self.log()

        if 'palette' in config:
            self.palette = read_key(config['palette'], int_keys=True)
            for n in self.palette:
                cp = self.palette[n].split()
                curses.init_pair(n, int(cp[0]), int(cp[1]))

        if 'colors' in config:
            self.colors = read_key(config['colors'], int_values=True)

        if 'styles' in config:
            self.styles = read_key(config['styles'])
            self.styles = {k: get_style(self.styles[k]) for k in self.styles}

        if 'icon' in config:
            self.icon = read_icon(config['icon'])
            self.draw_icon()

    def draw_borders(self):
        '''
            Draws window borders on the main screen.
        '''
        # info box borders
        for i in range(self.vw):
            self.scr.addch(self.vh, i, '=')
            self.scr.addch(self.h - 1, i, '=')
        for i in range(self.vh, self.h):
            self.scr.addch(i, 0, '"')

        # sidebar border
        for i in range(self.h):
            self.scr.addch(i, self.vw, '|')

        # display box border
        for i in range(self.vw, self.w):
            self.scr.addch(self.vh, i, '-')
            self.scr.addch(self.h - 1, i, '-')
        for i in range(self.vh, self.h):
            self.scr.addch(i, self.w - 1, '|')

        # decoration on corners
        self.scr.addch(self.vh, 0, '"')
        self.scr.addch(self.vh, self.vw, '"')
        self.scr.addch(self.h - 1, 0, '"')
        self.scr.addch(self.h - 1, self.vw, '"')
        self.scr.addch(self.vh, self.w - 1, '~')
        self.scr.addch(self.h - 1, self.w - 1, '`')
        self.scr.refresh()

    def format(self, c):
        formatting = 0
        if self.colors is not None and c in self.colors:
            cp = curses.color_pair(self.colors[c])
            formatting = formatting | cp
        if self.styles is not None and c in self.styles:
            formatting = formatting | self.styles[c]
        return formatting

    def render_map(self):
        '''
            Reloads world map info into the vis pad.
        '''
        if self.world is None: return
        h = len(self.world)
        w = len(self.world[0])
        self.vis = curses.newpad(h + 2 * self.margin_h, w + 2 * self.margin_w)

        #for i in range(h + 2 * self.margin_h):
        #    for j in range(w + 2 * self.margin_w):
        #        self.vis.addch(i, j, '=')
        
        for i in range(h):
            for j in range(w):
                char = self.world[i][j]
                self.vis.addch(i + self.margin_h, j + self.margin_w,
                               char if self.key is None else (self.key[char] if char in self.key else char),
                               self.format(char))

    def move(self, pos=None):
        '''
            Moves to a specified coordinate in the world map.
        '''
        if self.world is None: return
        if self.x != -1 and self.y != -1:
            c = self.world[self.y][self.x]
            self.vis.addch(self.y + self.margin_h, self.x + self.margin_w,
                           self.key[c] if self.key is not None and c in self.key else c,
                           self.format(c))

        if pos is not None:
            self.y = pos[0]
            self.x = pos[1]
        self.vis.addch(self.y + self.margin_h, self.x + self.margin_w, '@',
                       self.format('self'))
        
        self.vis.refresh(self.y, self.x,
                         0, 0, self.vh - 1, self.vw - 1)

    def log(self, text=None):
        '''
            Displays text in the infobox.
        '''
        if text is not None:
            self.text = text
        if self.text is None: return
        self.info.addstr(0, 0, self.text)
        self.info.clrtobot()
        self.info.refresh()

    def side_log(self, text=None):
        '''
            Displays text in the sidebar.
        '''
        if text is not None:
            self.sidetext = text
        if self.sidetext is None: return
        self.sidebar.addstr(0, 0, self.sidetext)
        self.sidebar.clrtobot()
        self.sidebar.refresh()

    def draw_icon(self):
        '''
            Redraws icon box.
        '''
        if self.icon is None: return
        self.box.clear()
        for i in range(min(len(self.icon), self.info_h)):
            for j in range(min(len(self.icon[i]), self.side_w - 2)):
                # TODO: figure out this thing...
                self.box.addch(i, j, self.icon[i][j])
        self.box.refresh()

    def resize(self):
        '''
            Recalculates sizes and refreshes if necessary.
        '''
        h = min(curses.LINES, self.MAX_HEIGHT)
        w = min(curses.COLS, self.MAX_WIDTH)
        if self.h != h or self.w != w:
            self.h = h
            self.w = w
            self.margin_h = (self.h - self.info_h - 2)//2
            self.margin_w = (self.w - self.side_w - 1)//2
            self.vh = self.margin_h * 2 + 1
            self.vw = self.margin_w * 2 + 1
            self.refresh()

    def refresh(self):
        '''
            Refreshes and redraws all windows.
        '''
        self.vis = curses.newwin(self.vh, self.vw,
                                 0, 0)
        self.info = curses.newwin(self.info_h, self.vw - 4,
                                  self.vh + 1, 2)
        self.sidebar = curses.newwin(self.vh, self.side_w,
                                     0, self.vw + 1)
        self.box = curses.newwin(self.info_h, self.side_w - 1,
                                 self.vh + 1, self.vw + 1)
        
        self.draw_borders()
        self.move()
        self.log()
        self.side_log()
