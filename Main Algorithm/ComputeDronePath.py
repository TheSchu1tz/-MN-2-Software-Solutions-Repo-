import numpy
import math
import random
import keyboard
import os
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
    distMatrix = numpy.empty((len(coords)+1, len(coords)+1))
    for x, coord1 in enumerate(coords):
        for y, coord2 in enumerate(coords):
            distance = EuclideanDistance(coord1, coord2)
            distMatrix[x+1,y+1] = distance
    return distMatrix

# creates a random ordering of the coordinates
def CreateRandomOrder(coords):
    indices = []
    for i in range(len(coords)):
        indices.append(i + 1)
    indices.remove(1)   # remove the recharge point
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
    return round(cost, 1)

# computes the Euclidean distance between 2 coordinates
def EuclideanDistance(coord1, coord2):
    a = pow(coord2[0] - coord1[0], 2)
    b = pow(coord2[1] - coord1[1], 2)
    return math.sqrt(a + b)

# writes the order with the best cost to file according to the 
# output specifications 
def WriteSolution(filepath, bestCost, bestOrder):
    splitFile = os.path.splitext(filepath)
    outputPath = splitFile[0] + "_solution_" + str(int(bestCost)) + ".txt"
    outputFile = open(outputPath, "w")
    outputFile.write(f"{bestOrder}")
    outputFile.close()
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
            print(f"\t\t{curr_solution}m found at {round(end - start, 2)}s")
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
    print(f"\t\t{best_solution}m found at {round(end - start, 2)}s")

    random_path = []
    random_solution = float('inf')
    while (not stop):
        coord_indexes = [i for i in range(len(coordinates))]
        random_path, random_solution = compute_NN(coord_indexes, coordinates, True)
        if random_solution <= best_solution:
            end = time.time()
            print(f"\t\t{random_solution}m found at {round(end - start, 2)}s")
            best_solution = random_solution
            best_path = random_path

    return best_solution, best_path

if __name__ == "__main__":
    main()