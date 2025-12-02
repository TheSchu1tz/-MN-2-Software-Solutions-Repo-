class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
    def __str__(self):
        return f"[{self.row + 1:02},{self.col + 1:02}]"

    __repr__ = __str__