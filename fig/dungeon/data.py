import json

def load(f):
    '''
        Loads a config file.
    '''
    config = json.load(open(f, 'r'))

def read_map(f):
    world = []
    lines = [l.strip() for l in open(f, 'r').readlines()]
    for l in lines:
        world.append([c for c in line])
    return world
