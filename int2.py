from dataclasses import dataclass
 
@dataclass
class int2:
    x: int = 0
    y: int = 0
 
    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return int2(self.x + other.x, self.y + other.y)
 
    def __sub__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return int2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) != int:
            raise TypeError

        return int2(self.x * other, self.y * other)
  
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.x==other.x and self.y==other.y
    
    def tuple(self):
        return self.x, self.y
 
