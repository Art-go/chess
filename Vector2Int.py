from dataclasses import dataclass
 
@dataclass
class Vector2Int:
    x: int = 0
    y: int = 0
 
    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return Vector2Int(self.x + other.x, self.y + other.y)
 
    def __sub__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return Vector2Int(self.x - other.x, self.y - other.y)
 
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.x==other.x and self.y==other.y
    
    def tuple(self):
        return self.x, self.y
 