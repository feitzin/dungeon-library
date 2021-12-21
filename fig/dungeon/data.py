import json

def load(f):
    '''
        Loads a config object from a file.
    '''
    config = json.load(open(f, 'r'))
    return config

def read_map(f):
    '''
        Reads a world map file.
    '''
    world = []
    lines = [l.rstrip('\n') for l in open(f, 'r').readlines()]
    for l in lines:
        world.append([c for c in l])
    # TODO: add size checking
    return world

def read_icon(f):
    '''
        Reads an icon for the logo square.
    '''
    icon = [l.strip() for l in open(f, 'r').readlines()]
    return icon

def read_key(f, int_keys=False, int_values=False):
    '''
        Reads a key file in the format
          (key character) <tab> (description).
        If `int_keys` is passed, converts keys to integers; if `int_values` is
        passed, converts values to integers.
    '''
    key = {}
    for line in open(f, 'r').readlines():
        splits = line.strip().split('\t')
        if int_keys:
            try:
                splits[0] = int(splits[0])
            except:
                pass
        if int_values:
            try:
                splits[1] = int(splits[1])
            except:
                pass
        key[splits[0]] = splits[1]
    return key

def read_descriptions(f):
    '''
        Very similar to read_key. Reads description files in the format
          (name) <any number of tabs> (description).
    '''
    items = {}
    for line in open(f, 'r').readlines():
        splits = line.strip().split('\t')
        items[splits[0]] = splits[-1].strip()
    return items

def update_locations(f, world):
    '''
        Reads a file of location-defined items, e.g. unique object items, in
        the format
          (y) <tab> (x) <tab> (name)
        into an existing world array.
    '''
    for line in open(f, 'r').readlines():
        splits = line.strip().split()
        world[int(splits[0])][int(splits[1])] = splits[2]
