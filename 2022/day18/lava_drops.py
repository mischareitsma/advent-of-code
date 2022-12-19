class Drop:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.group: 'Group' = None

    def coords(self):
        return self.x, self.y, self.z

    def __eq__(self, other):
        if not type(other) is Drop:
            return False
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

class Group:

    def __init__(self):
        self.drops: list[Drop] = 0
    
    def merge(self, other: 'Group'):
        for drop in other.drops:
            drop.group = self
        
        del other
