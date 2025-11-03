import numpy
import math
import random
import keyboard
import os
import matplotlib.pyplot as plt
import time
import threading

def main():
    filepath = input("Enter the name of the file: ")

    # read the file
    lines = ReadFile(filepath)

    # parse the file and set up the list of coordinates
    coords = ParseFile(lines)
    
    # create distance matrix
    distMatrix = CreateDistanceMatrix(coords)

    # create random order of coordinates to visit
    # algType = algorithm to be run (1 = random, 2 = random prune, 3 = NN)
    algType = 3

    if algType == 1:
        indices = CreateRandomOrder(coords)
        bestCost = ComputeCost(indices, distMatrix)
        
    if algType == 2:
        bestCost, indices = prune_search(coords)

    if algType == 3:
        bestCost, indices = NN_random_search(coords)

    # set up variable to track best solution
    bestOrder = indices

    if algType == 1:
    # output intro text
        print("There are", len(coords), "nodes, computing route..")
        print("\tShortest Route Discovered So Far")
        print("\t\t", bestCost)

        # begin the main loop, looking for better answers
        while True:
            # handle ENTER press, anytime algorithm exits
            if (keyboard.is_pressed('\n')):
                outputPath = WriteSolution(filepath, bestCost, bestOrder, coords)
                print("Route written to disk as", outputPath)
                break
            # check if theres a better solution otherwise
            newOrder = CreateRandomOrder(coords)
            cost = ComputeCost(newOrder, distMatrix)
            if (cost < bestCost):
                bestCost = cost
                bestOrder = newOrder
                print("\t\t", bestCost)
    else:
        outputPath = WriteSolution(filepath, bestCost, bestOrder, coords)
        print("Route written to disk as", outputPath)

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

    # Test for matrix symmetry
    size = len(distMatrix)
    for i in range(size-1):
        for j in range(size-1, -1, -1):
            if (not math.isclose(distMatrix[i,j], distMatrix[j,i])):
                raise TypeError("Matrix not loaded correctly")

    return distMatrix

# creates a random ordering of the coordinates
def CreateRandomOrder(coords):
    indices = []
    for i in range(len(coords)):
        indices.append(i)
    indices.remove(0)   # remove the recharge point
    random.shuffle(indices)
    # guarantees landing pad to be at the beginning and end
    indices.insert(0, 0)
    indices.append(0)
    return indices

# computes the cost of a particular order using distance matrix
def ComputeCost(order, distMatrix):
    cost = 0.0
    for i in range(len(order) - 1):
        cost += distMatrix[order[i], order[i+1]]
    return round(cost, 1)

# computes the Euclidean distance between 2 coordinates
def EuclideanDistance(coord1, coord2):
    a = pow(coord2[0] - coord1[0], 2)
    b = pow(coord2[1] - coord1[1], 2)
    return math.sqrt(a + b)

# writes the order with the best cost to file according to the 
# output specifications 
def WriteSolution(filepath, bestCost, bestOrder, coordinates):
    splitFile = os.path.splitext(filepath)
    outputPath = splitFile[0] + "_solution_" + str(int(bestCost)) + ".txt"
    
    # create the txt file output
    outputFile = open(outputPath, "w")
    outputStr = ""  
    for index in bestOrder:
        outputStr += str(index + 1) + " "
    outputFile.write(f"{outputStr}")
    outputFile.close()

    # create the png output
    plt.figure(figsize=(19.20, 19.20), dpi=100)
    plt.rcParams.update({'font.size': 22})
    plt.title(f"Best Route Found (Distance = {int(bestCost)} units)", fontsize=32)
    plt.xlabel('X', fontsize=24)
    plt.ylabel('Y', fontsize=24)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.draw()

    landingX = 0
    landingY = 0
    x = []
    y = []
    for i in bestOrder:
        x.append(coordinates[i][0])
        y.append(coordinates[i][1])
        if i == 0:
            landingX = coordinates[i][0]
            landingY = coordinates[i][1]
    plt.plot(x, y, color='blue', linewidth=2, marker='o', markersize=10)
    plt.plot(landingX, landingY, color='red', marker='o', markersize=16)
    plt.tight_layout()
    plt.savefig(splitFile[0] + "_solution_" + str(int(bestCost)) + ".png", dpi=100)

    return outputPath

#MO: Need this to end execution on enter keystroke. REQUIRED FOR MACOS
stop = False
def wait_for_key():
    global stop
    input()
    stop = True

#MO: This is a modified basic search that incorporates pruning whenever a distance 
#MO: found is greater than the current best solution
def prune_search(coordinates: list):

    best_solution = float("inf")
    #best_path = coordinates.copy()
    best_path = []
    coord_indexes = [i for i in range(len(coordinates))]

    pruned = False

    start = time.time() #MO: This is to time the search

    threading.Thread(target=wait_for_key, daemon=True).start()

    print("There are", len(coordinates), "nodes, computing route..")
    print("\tShortest Route Discovered So Far")
    while(not stop):
        curr_solution = 0.0
        trees_coords = coord_indexes[1:].copy()
        random.shuffle(trees_coords)
        curr_path = [0] + trees_coords + [0]
        pruned = False

        for i in range(len(curr_path) - 1):
            left = coordinates[curr_path[i]]
            right = coordinates[curr_path[i+1]]
            curr_solution += math.dist(left, right)
            if curr_solution >= best_solution:
                pruned = True
                break
        
        if curr_solution < best_solution and not pruned:
            end = time.time()
            print(f"\t\t{round(curr_solution, 1)}") #m found at {round(end - start, 2)}s
            best_solution = curr_solution
            best_path = curr_path.copy()
        
    return best_solution, best_path

#MO: This function computes the nearest neighbor path. 
##   If randomize is True, it will do a nearest neighbor with a random chance of deviation.
def compute_NN(coord_indexes:list, coordinates:list, randomize:bool):
    nn_path = [0]
    visited = set()
    visited.add(0)
    nn_solution = 0

    current_index = 0

    for _ in range(len(coord_indexes)):
        first_closest_index = None
        first_closest_dist = float('inf')
        second_closest_index = None
        second_closest_dist = float('inf')
        for j in coord_indexes:

            if j not in visited and j != current_index:
                left = coordinates[current_index]
                right = coordinates[j]
                left_right_dist = math.dist(left, right)

                if left_right_dist < first_closest_dist:
                    second_closest_dist = first_closest_dist
                    second_closest_index = first_closest_index
                    first_closest_index = j
                    first_closest_dist = left_right_dist
                elif left_right_dist < second_closest_dist:
                    second_closest_dist = left_right_dist
                    second_closest_index = j
                    
        if first_closest_index is None:
            break
        if randomize and second_closest_index is not None and random.random() < 0.1:
            closest_index = second_closest_index
            closest_distance = second_closest_dist
        else:
            closest_index = first_closest_index
            closest_distance = first_closest_dist

        visited.add(closest_index)
        nn_path.append(closest_index)
        nn_solution += closest_distance
        current_index = closest_index
    
    nn_solution += math.dist(coordinates[0], coordinates[current_index])
    nn_path.append(0)
    return nn_path, nn_solution

#MO: This function performs a nearest neighbor search with random path variation
def NN_random_search(coordinates: list):

    best_solution = float("inf")
    best_path = []
    coord_indexes = [i for i in range(len(coordinates))]

    start = time.time() #MO: This is to time the search

    threading.Thread(target=wait_for_key, daemon=True).start()

    #MO: Compute NN path
    nn_path, nn_solution = compute_NN(coord_indexes, coordinates, False)
    #MO: Set our baseline as the nn_solution and begin modified search
    best_path = nn_path.copy()
    best_solution = nn_solution 

    end = time.time()

    random_path = []
    random_solution = float('inf')
    print("There are", len(coordinates), "nodes, computing route..")
    print("\tShortest Route Discovered So Far")
    print(f"\t\t{round(nn_solution, 1)}")
    while (not stop):
        coord_indexes = [i for i in range(len(coordinates))]
        random_path, random_solution = compute_NN(coord_indexes, coordinates, True)
        if random_solution <= best_solution:
            end = time.time()
            print(f"\t\t{round(random_solution, 1)}")#m found at {round(end - start, 2)}s
            best_solution = random_solution
            best_path = random_path

    return best_solution, best_path

if __name__ == "__main__":
    main()