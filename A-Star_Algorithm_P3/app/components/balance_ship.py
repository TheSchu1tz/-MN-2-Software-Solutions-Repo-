import numpy
from data_types.coordinate import Coordinate
from data_types.container import Container

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
    mid_col = GRID_COLS // 2

    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            container:Container = grid[y][x]
            if container and container.item != UNUSED and container.item != NAN:
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
    
    #Calculate sum of left/right weights
    sumLeft = sum(left_weights)
    sumRight = sum(right_weights)
    
    # Balance Case 1: difference less than 10% limit
    if TenPercentBalanceHelper(sumLeft, sumRight):
        return True

    # Balance Case 2: difference is minimal
    if MinDiffBalanceHelper(sumLeft, sumRight, all_weights):
        return True

    # If neither, return false
    return False

# CheckBalance helper for first balanced case
def TenPercentBalanceHelper(sumLeft: int, sumRight: int):
    total = sumLeft + sumRight
    difference = abs(sumLeft - sumRight)
    limit = total * 0.10
    return difference <= limit

# CheckBalance helper for second balanced case
def MinDiffBalanceHelper(sumLeft: int, sumRight: int, all_weights: int):
    difference = abs(sumLeft - sumRight)
    total_weight = sum(all_weights)
    target = total_weight / 2

    possible_sums = {0}

    for weight in all_weights:
        possible_sums |= {s + weight for s in possible_sums}

    best_half_sum = max(s for s in possible_sums if s <= target)
    possible_min_diff = total_weight - best_half_sum - best_half_sum
    return difference == possible_min_diff

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
        item = parts[2].strip()

        container = Container(coord, weight, item)
        manifest.append(container)
    return manifest

# TEST MAIN
# def main():
#     print("--Test 1: 0 Containers Balanced (True, Special Case 1)--")
#     fake_manifest_1 = [
#         "[01,01], {00000}, UNUSED",
#         "[01,12], {00000}, UNUSED"
#     ]
#     manifest_1 = ParseFile(fake_manifest_1)
#     grid_1 = CreateGrid(manifest_1)
#     print(f"Result 1: {CheckBalance(grid_1)}")

#     print("--Test 2: 1 Container Balanced (True, Special Case 2)--")
#     fake_manifest_2 = [
#         "[01,01], {00100}, Place1",
#         "[01,12], {00000}, UNUSED"
#     ]
#     manifest_2 = ParseFile(fake_manifest_2)
#     grid_2 = CreateGrid(manifest_2)
#     print(f"Result 2: {CheckBalance(grid_2)}")

    
#     print("--Test 3: 2 Container Balanced (True, Special Case 3)--")
#     fake_manifest_3 = [
#         "[01,01], {00100}, Place1",
#         "[01,12], {01000}, Place2"
#     ]
#     manifest_3 = ParseFile(fake_manifest_3)
#     grid_3 = CreateGrid(manifest_3)
#     print(f"Result 3: {CheckBalance(grid_3)}")

#     print("--Test 4: 2 Container Unbalanced (False, Both Same Side)--")
#     fake_manifest_4 = [
#         "[01,01], {00100}, Place1",
#         "[01,02], {01000}, Place2"
#     ]
#     manifest_4 = ParseFile(fake_manifest_4)
#     grid_4 = CreateGrid(manifest_4)
#     print(f"Result 4: {CheckBalance(grid_4)}")

#     print("--Test 5: 5 Container Balanced (True, Within 10%)--")
#     fake_manifest_5 = [
#         "[01,01], {00100}, Place1",
#         "[02,01], {00100}, Place2",
#         "[01,02], {00100}, Place3",
#         "[01,12], {00150}, Place4",
#         "[01,11], {00130}, Place5"
#     ]
#     manifest_5 = ParseFile(fake_manifest_5)
#     grid_5 = CreateGrid(manifest_5)
#     print(f"Result 5: {CheckBalance(grid_5)}")

#     print("--Test 6: 5 Container Balanced (True, Difference Is Minimal (300-200))--")
#     fake_manifest_6 = [
#         "[01,01], {00100}, Place1",
#         "[02,01], {00100}, Place2",
#         "[01,02], {00100}, Place3",
#         "[01,12], {00100}, Place4",
#         "[01,11], {00100}, Place5"
#     ]
#     manifest_6 = ParseFile(fake_manifest_6)
#     grid_6 = CreateGrid(manifest_6)
#     print(f"Result 6: {CheckBalance(grid_6)}")

#     print("--Test 7: 5 Container Unbalanced (False, Not 10% Or Minimal (400-100))--")
#     fake_manifest_7 = [
#         "[01,01], {00100}, Place1",
#         "[02,01], {00100}, Place2",
#         "[01,02], {00100}, Place3",
#         "[02,02], {00100}, Place4",
#         "[01,12], {00100}, Place5"
#     ]
#     manifest_7 = ParseFile(fake_manifest_7)
#     grid_7 = CreateGrid(manifest_7)
#     print(f"Result 7: {CheckBalance(grid_7)}")

    
# if __name__ == "__main__":
#     main()