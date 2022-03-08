import json

def read_json(path):
    f = open(path)
    vars_dict = json.load(f)
    return vars_dict

def write_json(path, var, replacement):
    f = open(path)
    vars_dict = json.load(f)
    f.close()
    del(f)
    
    f = open(path, 'w')

    vars_dict[var] = replacement
    json.dump(vars_dict, f)
