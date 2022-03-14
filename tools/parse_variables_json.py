import json

def read_json(path):
    f = open(path)
    vars_dict = json.load(f)
    return vars_dict

def write_json(path, replacement):
    f = open(path, 'w')
    # vars_dict[var] = replacement
    json.dump(replacement, f)
