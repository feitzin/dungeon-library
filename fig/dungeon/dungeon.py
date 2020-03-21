from data import read_map, load

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
    
    def __init__(self, config=None):
        self.mode = self.WORLD_MODE
        self.x = -1
        self.y = -1

        
