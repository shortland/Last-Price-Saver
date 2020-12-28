import json


def read_refresh_token(path):
    with open(path) as f:
        return json.load(f).get('refresh_token')
