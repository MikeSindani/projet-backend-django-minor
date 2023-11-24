import json


class Domain:
    def __init__(self):
        self.R = 'RandomWords()'
    def do(self):
        word = 'lea'
        return json.dumps({"message": word})

