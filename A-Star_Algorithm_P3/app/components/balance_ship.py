import numpy
from components.data_types.coordinate import Coordinate
from components.data_types.container import Container

GRID_ROWS = 8
GRID_COLS = 12

UNUSED = "UNUSED"
NAN = "NAN"

def MoveToColumn(grid:numpy.ndarray, container:Container, newColumn:int):
    # TODO: create a copy of the grid aka node
    
    # find the highest empty space in the new column
    for i in range(GRID_ROWS):
        check:Container = grid[i][newColumn]
        if check.item == UNUSED:
            emptySpace = check
            break

    # calculate cost of swap
    costSwap = CostSwap(grid, container.coord.col, newColumn)

    # swap empty and containers positions above it
    emptyCoord = emptySpace.coord
    currCoord = container.coord
    grid[currCoord.row][currCoord.col] = emptySpace
    grid[emptyCoord.row][emptyCoord.col] = container

    return costSwap

# returns the amount the crane needs to move to get from col1 to col2
def CostSwap(grid, col1, col2):
    raise NotImplementedError("need to implement this!")

def Height(grid:numpy.ndarray, column):
    height = 0
    for i in range(GRID_ROWS):
        container:Container = grid[i][column]
        if (container.item == UNUSED): # empty space, no items above it
            return height
        elif (container.item != NAN):  # non-empty, non-null space
            height += 1
    return height

def CheckBalance(grid:numpy.ndarray):
    # Get Weights
    left_weights = []
    right_weights = []
    mid_col = GRID_COLS / 2

    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            container:Container = grid[x][y]
            if container.item != UNUSED and container.item != NAN:
                if x < mid_col:
                    left_weights.append(container.weight)
                else:
                    right_weights.append(container.weight)

    all_weights = left_weights + right_weights
    
    # Special Case 1 & 2: 0 or 1 containers only
    if len(all_weights) <= 1:
        return True
    
    # Special Case 3: 2 containers, 1 each side
    if len(left_weights) == 1 and len(right_weights) == 1:
        return True
    
    # Case 1: difference less than limit
    # sum the left and right halves
    sumLeft = sum(left_weights)
    sumRight = sum(right_weights)
    total = sumLeft + sumRight
    difference = abs(sumLeft - sumRight)
    limit = total * 0.10

    if (difference < limit):
        return True

    # Case 2: difference is minimal
    # determine minimal difference

    


def CreateGrid(manifest):
    grid = numpy.zeros((GRID_ROWS, GRID_COLS), dtype=Container)
    for i in range(len(manifest)):
        coord:Coordinate = manifest[i].coord
        grid[coord.row, coord.col] = manifest[i]
    return grid

# returns array of strings read from filename
def ReadFile(filename):
    file = open(filename, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

# creates data representation of manifest
def ParseFile(lines):
    manifest = []
    for line in lines:
        # get plain text [01, 01], {00000}, NAN
        parts = line.split(", ")
        # get int representation of the coordinate [1,1]
        x, y = parts[0].strip("[]").split(",")
        coord = Coordinate(int(x) - 1, int(y) - 1)
        # get the id "{00000}"
        weight = int(parts[1].strip("{}"))
        # get the item "NAN"
        item = parts[2].strip("\n")

        container = Container(coord, weight, item)
        manifest.append(container)
    return manifest