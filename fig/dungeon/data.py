import json

def load(f):
    '''
        Loads a config object from a file.
    '''
    config = json.load(open(f, 'r'))
    return config

def read_map(f):
    world = []
    lines = [l.strip() for l in open(f, 'r').readlines()]
    for l in lines:
        world.append([c for c in l])
    # TODO: add size checking
    return world

def read_icon(f):
    icon = [l.strip() for l in open(f, 'r').readlines()]
    return icon
