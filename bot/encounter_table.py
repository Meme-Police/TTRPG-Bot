import json

class EncounterTable():
    def __init__(self, table = [], owner = 0):
        self.table = table
        self.owner = owner
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def addItem(self, item):
        self.table.append(item)
    
    def removeItem(self, item):
        del self.table[item]
    
    def displayTable(self):
        table_string = "```"
        i = 1
        for item in self.table:
            table_string += (f"\n{i}: {item}")
            i += 1
        table_string += "\n```"
        return table_string

        
def fromJson(json_string):
    json_object = json.loads(json_string)
    return EncounterTable(json_object["table"], json_object["owner"])