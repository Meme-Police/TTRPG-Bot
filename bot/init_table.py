import json
class Table():
    def __init__(self, table = {}, position = None, max_pos = 20):
        self.table = table
        self.position = position
        self.max_pos = max_pos
        
    def _getFromPos(self):
        items = self.table.items()
        people_list = []
        for name, init in items:
            if (init == self.position):
                people_list.append(name)
        return people_list
        
    def toString(self):
        init_list = [None for x in range(20)]
        display_string = "```\n"
        for (name, pos) in self.table.items():
            if (pos >= len(init_list)):
                extention = [None for x in range(pos-20)]
                extention[-1] = [name]
                init_list.extend(extention)
            elif(init_list[pos-1] != None):
                init_list[pos-1].append(name)
            else:
                init_list[pos-1] = [name]
        i = len(init_list) -1
        while(i >= 0):
            # TODO: Format better
            if (i+1 == self.position):
                display_string += "-> "
            substring = ""
            if (init_list[i] != None):
                substring = ", ".join(init_list[i])
                substring.replace("'", "")
            display_string += str(f"{i+1}: {substring}\n")
            i -= 1
        display_string += "```"
        return display_string
            
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def next(self):
        if (self.position == None) or (self.position == 1):
            self.position = self.max_pos
        else:
            self.position -= 1
        return self._getFromPos()
    def current(self):
        return self._getFromPos()
            
    def insert(self, name, pos):
        self.table.update({name: pos})
        if (pos > self.max_pos):
            self.max_pos = pos
    def remove(self, name):
        # We do not care if the item is not present
        self.table.pop(name, '')
        if (bool(self.table) == False):
            self.max_pos = None
        else:
            values = self.table.values()
            self.max_pos = max(values)
        
    def clear(self):
        self.table = {}
    
def fromJson(string):
    json_object = json.loads(string)
    return Table(json_object["table"], json_object["position"], json_object["max_pos"])
