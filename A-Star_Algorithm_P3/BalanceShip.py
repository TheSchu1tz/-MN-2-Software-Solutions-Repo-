from collections import defaultdict
import numpy

def main():
    filepath = input("Please provide the file to solve for: ")
    file = ReadFile(filepath)
    manifest = ParseFile(file)
    startGrid = CreateGrid(manifest)

def MoveToColumn(item, newColumn):
    currColumn = item[0][1]

def Height(grid, column):
    height = 0
    for i in range(8):
        item = grid[i][column]
        if (item[2] == "UNUSED"): # empty space, no items above it
            return height
        elif (item[2] != "NAN"):  # non-empty, non-null space
            height += item[1]
        return height

def CheckBalance(grid):
    # Case 1: difference less than limit
    # sum the left and right halves
    sumLeft = 0
    sumRight = 0
    for i in range(8):
        for j in range(6):
            leftItem = grid[i][j]
            rightItem = grid[i][6 + j]
            sumLeft += leftItem[1]
            sumRight += rightItem[1]

    difference = abs(sumLeft - sumRight)
    limit = sumLeft + sumRight * 0.10

    return difference < limit or difference == 0

    # TODO: Case 2: difference is minimal

def CreateGrid(manifest):
    grid = numpy.zeros((8, 12), dtype=type(manifest[0]))
    for i in range(len(manifest)):
        coord = manifest[i][0]
        grid[coord[0] - 1, coord[1] - 1] = manifest[i]
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
        coord = [int(x), int(y)]
        # get the id "{00000}"
        weight = int(parts[1].strip("{}"))
        # get the item "NAN"
        item = parts[2].strip("\n")

        entry = [coord, weight, item]
        manifest.append(entry)
    return manifest

if __name__ == "__main__":
    main()