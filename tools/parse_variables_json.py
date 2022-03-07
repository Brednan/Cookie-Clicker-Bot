import json

def read_json(path):
    f = open(path)
    vars_dict = json.load(f)
    return vars_dict()
