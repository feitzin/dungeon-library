import json

def load(f):
    '''
        Loads a config object from a file.
    '''
    config = json.load(open(f, 'r'))
    return config

def read_map(f):
    world = []
    lines = [l.rstrip('\n') for l in open(f, 'r').readlines()]
    for l in lines:
        world.append([c for c in l])
    # TODO: add size checking
    return world

def read_icon(f):
    icon = [l.strip() for l in open(f, 'r').readlines()]
    return icon

def read_key(f):
    key = {}
    for line in open(f, 'r').readlines():
        splits = line.strip().split('\t')
        key[splits[0]] = splits[1]
    return key
