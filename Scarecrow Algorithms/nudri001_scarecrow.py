import numpy
import math
import random
import keyboard
import os

def main():
    filepath = input("Enter the name of the file: ")

    # read the file
    lines = ReadFile(filepath)

    # parse the file and set up the list of coordinates
    coords = ParseFile(lines)
    
    # create distance matrix
    distMatrix = CreateDistanceMatrix(coords)

    # create random order of coordinates to visit
    indices = CreateRandomOrder(coords)

    # set up variables to track best solution
    bestCost = ComputeCost(indices, distMatrix)
    bestOrder = indices

    # output intro text
    print("There are", len(coords), "nodes, computing route..")
    print("\tShortest Route Discovered So Far")
    print("\t\t", bestCost)

    # begin the main loop, looking for better answers
    while True:
        # handle ENTER press, anytime algorithm exits
        if (keyboard.is_pressed('\n')):
            outputPath = WriteSolution(filepath, bestCost, bestOrder)
            print("Route written to disk as", outputPath)
            break
        # check if theres a better solution otherwise
        newOrder = CreateRandomOrder(coords)
        cost = ComputeCost(newOrder, distMatrix)
        if (cost < bestCost):
            bestCost = cost
            bestOrder = newOrder
            print("\t\t", bestCost)

# returns array of strings read from filename
def ReadFile(filename):
    file = open(filename, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

# parses IEEE numbers formatted accorded to input specs
# returns (x,y) list of coordinates from file contents
def ParseFile(lines):
    coords = []
    for line in lines:
        numbers = line.split("   ")
        while '' in numbers:
            numbers.remove('')
        x = float(numbers[0].strip())
        y = float(numbers[1].strip())
        coord = [x, y]
        coords.append(coord)
    return coords

# Create distance matrix using Euclidean Distance from coordinates
def CreateDistanceMatrix(coords):
    distMatrix = numpy.empty((len(coords), len(coords)))
    for x, coord1 in enumerate(coords):
        for y, coord2 in enumerate(coords):
            distance = EuclideanDistance(coord1, coord2)
            distMatrix[x,y] = distance
    return distMatrix

# creates a random ordering of the coordinates
def CreateRandomOrder(coords):
    indices = []
    for i in range(len(coords)):
        indices.append(i)
    indices.remove(1)
    random.shuffle(indices)
    # guarantees 1 to be at the beginning and end
    indices.insert(0, 1)
    indices.append(1)
    return indices

# computes the cost of a particular order using distance matrix
def ComputeCost(order, distMatrix):
    cost = 0.0
    for i in range(len(order) - 1):
        cost += distMatrix[order[i], order[i+1]]
    return int(cost)

# computes the Euclidean distance between 2 coordinates
def EuclideanDistance(coord1, coord2):
    a = pow(coord2[0] - coord1[0], 2)
    b = pow(coord2[1] - coord1[1], 2)
    return math.sqrt(a + b)

# writes the order with the best cost to file according to the 
# output specifications 
def WriteSolution(filepath, bestCost, bestOrder):
    splitFile = os.path.splitext(filepath)
    outputPath = splitFile[0] + "_solution_" + str(bestCost) + ".txt"
    outputFile = open(outputPath, "w")
    outputFile.write(f"{bestOrder}")
    outputFile.close()
    return outputPath

if __name__ == "__main__":
    main()