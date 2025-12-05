from components.data_types.coordinate import Coordinate

class Container:
    def __init__(self, coord:Coordinate, weight:int, item:str):
        self.coord = coord
        self.weight = weight
        self.item = item