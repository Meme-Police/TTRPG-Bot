import json

class ShopTable():
    def __init__(self, table = [], owner = 0):
        self.table = table
        self.owner = owner
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def addItem(self, name, price, description):
        self.table.append((name, price, description))
    
    def removeItem(self, item):
        del self.table[item]
    
    def displayTable(self):
        table_string = "```"
        i = 1
        for (name, price, description) in self.table:
            table_string += (f"\n{name} {price}: {description}")
            i += 1
        table_string += "\n```"
        return table_string

        
def fromJson(json_string):
    json_object = json.loads(json_string)
    return ShopTable(json_object["table"], json_object["owner"])