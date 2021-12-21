from data import read_map, read_key, read_descriptions, update_locations
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

    MOVABLE = ['m', 'd', 'f', 's']
    SITTABLE = ['s']
    INTERACTIVE = []
    GATE = ['g']
    
    def __init__(self, display=None, config=None):
        '''
            Basic initialization.
        '''
        self.mode = self.WORLD_MODE
        self.x = -1
        self.y = -1
        self.direction = None
        self.world = None
        self.data = None
        self.w = 0
        self.h = 0

        self.movability = None
        self.objects = None
        self.generic = None

        if display is not None:
            self.display = display
            self.display.load(config)
        else:
            self.display = DungeonDisplay()

        if config is not None:
            self.load(config)

    def load(self, config):
        '''
            Load a config specification.
        '''
        # read world map
        if 'map' in config:
            self.world = read_map(config['map'])
            self.data = read_map(config['map'])
            self.w = len(self.world[0])
            self.h = len(self.world)

        # set default starting position
        if 'pos' in config and self.world is not None:
            self.y = config['pos'][0]
            self.x = config['pos'][1]

        # add movability information
        if 'movability' in config:
            self.movability = read_key(config['movability'])

        # add unique object key
        if 'objects' in config:
            self.objects = read_descriptions(config['objects'])

        # add generic object key
        if 'generic' in config:
            self.generic = read_key(config['generic'])

        # add special locations to world map
        if 'spec' in config:
            update_locations(config['spec'], self.data)

    def move(self, key, debug=False):
        '''
            Processes a move action.
        '''
        if self.world is None:
            return
        
        if key == self.LEFT:
            offset = [0, -1]
            if debug: self.display.side_log('left')
        elif key == self.RIGHT:
            offset = [0, 1]
            if debug: self.display.side_log('right')
        elif key == self.UP:
            offset = [-1, 0]
            if debug: self.display.side_log('up')
        elif key == self.DOWN:
            offset = [1, 0]
            if debug: self.display.side_log('down')
        else:
            return

        ny = self.y + offset[0]
        nx = self.x + offset[1]

        # skip if invalid
        if nx < 0 or nx >= self.w:
            return
        if ny < 0 or ny >= self.h:
            return

        # if we can move, then move
        if self.world[ny][nx] in self.movability:
            if self.movability[self.world[ny][nx]] in self.MOVABLE:
                self.y = ny
                self.x = nx
                # TODO: ambience
                self.display.move([self.y, self.x])
                self.direction = offset
                return

        # otherwise, try an off-location activation
        self.activate(ny, nx, key)

    def activate(self, y, x, key, debug=False):
        '''
            Off-coordinate location activation.
        '''
        if self.world is None:
            return
        
        # skip if invalid
        if x >= self.w or y >= self.h:
            return

        o = self.data[y][x]
        t = self.world[y][x]
        if debug: self.display.side_log(str(self.y) + ',' + str(self.x) + '\n' + str(y) + ',' + str(x) + '\n' + o)

        # desplay description for unique object
        if o in self.objects:
            self.display.log(self.objects[o])

        # otherwise, display description for generic object type, if it exists
        elif t in self.generic:
            if self.generic[t][0] in ['a', 'e', 'i', 'o', 'u']:
                self.display.log("It's an " + self.generic[t] + ".")
            else:
                self.display.log("It's a " + self.generic[t] + ".")

    def look(self):
        '''
            Looks around.
        '''
        if self.world is None:
            return
        pass # TODO: describe region

    def act(self):
        '''
            On-coordinate location activation.
        '''
        if self.world is None:
            return
        pass # TODO: interact with current facing direction, if available; otherwise, default to off-coordinate activation
