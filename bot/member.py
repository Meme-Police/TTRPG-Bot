import json
# The member object
class Member():
    def __init__(self, id, health, spells):
        self.id = id
        self.health = health
        self.spells = spells
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        
        