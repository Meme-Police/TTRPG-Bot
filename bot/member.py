import json
# The member object
class Member():
    def __init__(self, id, max_health, health, max_spells, spells):
        self.id = id
        self.max_health = max_health
        self.health = health
        self.max_spells = max_spells
        self.spells = spells
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
def fromJson(json_string):
    json_object = json.loads(json_string)
    return Member(json_object["id"], json_object["max_health"], json_object["health"], json_object["max_spells"], json_object["spells"])
    
        