import json

class EncounterTable():
    def __init__(self, table = {}, owner = 0):
        self.table = table
        self.owner = owner
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        
def fromJson(json_string):
    json_object = json.loads(json_string)
    return EncounterTable(json_object["table"], json_object["owner"])