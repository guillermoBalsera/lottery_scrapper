import json


def read_file(source):
    with open(f"./downloads/{source}.json", 'r') as f:
        return json.load(f)
