import random
import math
import time
import os

#MO: This is a basic search that searching random permutations of the path to find the optimal one
def dumb_search(coordinates: list):

    best_solution = float("inf")
    best_path = coordinates

    start = time.time() #MO: This is to time the search

    try:
        while(True):
            curr_solution = 0
            trees_coords = coordinates[1:-1]
            random.shuffle(trees_coords)
            coordinates[1:-1] = trees_coords
            for i in range(len(coordinates) - 1):
                left = coordinates[i]
                right = coordinates[i+1]
                curr_solution += math.dist(left, right)
            
            if curr_solution < best_solution:
                end = time.time()
                print(f"\t\t{curr_solution}m found at {round(end - start, 2)}s")
                best_solution = curr_solution
                best_path = coordinates
    except:
        KeyboardInterrupt
        return best_solution, best_path

#MO: This is a modified basic search that incorporates pruning whenever a distance 
#MO: found is greater than the current best solution
def prune_search(coordinates: list):

    best_solution = float("inf")
    best_path = coordinates
    pruned = False

    start = time.time() #MO: This is to time the search

    try:
        while(True):
            curr_solution = 0
            trees_coords = coordinates[1:-1]
            random.shuffle(trees_coords)
            coordinates[1:-1] = trees_coords
            for i in range(len(coordinates) - 1):
                left = coordinates[i]
                right = coordinates[i+1]
                left_right_dist = math.dist(left, right)
                if left_right_dist >= best_solution:
                    pruned = True
                    break
                curr_solution += left_right_dist
            
            if curr_solution < best_solution and not pruned:
                end = time.time()
                print(f"\t\t{curr_solution}m found at {round(end - start, 2)}s")
                best_solution = curr_solution
                best_path = coordinates
            pruned = False
    except:
        KeyboardInterrupt
        return best_solution, best_path

if __name__=="__main__":

    filename = input("Enter the name of file: ")

    coordinates = []

    with open(filename, 'r') as file:
        for line in file:
            x, y = tuple(map(float, line.split()))
            coordinates.append((x,y))
    
    print(f"There are {len(coordinates)} nodes, calculating route..\n\tShortest Route Discovered So Far")
    #best_solution, best_path = dumb_search(coordinates)
    best_solution, best_path = prune_search(coordinates)
    solution_filename = "test_solutions/" + os.path.basename(filename) + "_solution_" + str(best_solution) + ".txt"

    with open(solution_filename, 'w') as f:
        for x,y in best_path:
            f.write(str(x) + " " + str(y) + "\n")

    print(f"Route written to disk as test_solutions/{os.path.basename(filename)}_solution_{best_solution}.txt")
    
    
            
    
    