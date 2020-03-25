from data import read_map, load
from graphics import DungeonDisplay

class Dungeon():
    '''
        Internal model class for the dungeon.
    '''
    # class constants
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    WORLD_MODE = 0
    SIDE_MODE = 1
    
    def __init__(self, display=None, config=None):
        self.mode = self.WORLD_MODE
        self.x = -1
        self.y = -1
        self.world = None
        self.w = 0
        self.h = 0

        if display is not None:
            self.display = display
        else:
            self.display = DungeonDisplay()

        pass

    def load(self, config):
        pass # TODO

    def move(self, key):
        '''
            Processes a move action.
        '''
        if self.world is None:
            return
        
        if key == self.LEFT:
            offset = [0, -1]
        elif key == self.RIGHT:
            offset = [0, 1]
        elif key == self.UP:
            offset = [1, 0]
        elif key == self.DOWN:
            offset = [-1, 0]
        else:
            return

        nx = self.x + offset[0]
        ny = self.y + offset[1]

        # check if valid
        if nx < 0 or nx > self.w:
            return
        if ny < 0 or ny > self.h:
            return

        if self.world[ny][nx] in self.movable:
            self.y = ny
            self.x = nx
            return

        self.activate(ny, nx, key)

    def activate(self, x, y, key):
        '''
            Off-coordinate location activation.
        '''
        pass # TODO

    def look(self):
        '''
            Looks around.
        '''
        if self.world is None:
            return
        pass # TODO

    def act(self):
        '''
            On-coordinate location activation.
        '''
        if self.world is None:
            return
        pass # TODO
