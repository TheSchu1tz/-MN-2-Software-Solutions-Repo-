import numpy
import math
import random
import keyboard
import os
import matplotlib.pyplot as plt
import time
import threading
from collections import defaultdict

def main():
    filepath = input("Enter the name of file: ")

    # read the file
    lines = ReadFile(filepath)

    # parse the file and set up the list of coordinates
    coords = ParseFile(lines)
    all_coords_only = [item[0] for item in coords]
    original_indices_map = {tuple(item[0]): item[1] + 1 for item in coords}

    # output intro text
    future_time_struct = time.time() + (5 * 60)
    future_local_time = time.localtime(future_time_struct)
    finish_time_hm = time.strftime("%I:%M%p", time.localtime(time.time() + (5 * 60))).lower()
    print(f"There are", len(coords), "nodes: Solutions will be available by " + finish_time_hm)
    all_solutions = {}
    drone_counts = [1, 2, 3, 4]
    #NS: For loop to find all possible drone solutions and output
    for k in drone_counts:
        cluster_centers, cluster_data = KMeans_Classify(all_coords_only, k)
        total_distance = 0.0
        solutions = []
        for i in range(k):
            cluster_coords = cluster_data.get(i, [])
            landing_coord = cluster_centers[i]
            if not cluster_coords:
                route_length = 0.0
                full_path = [landing_coord, landing_coord]
            else:
                route_length, full_path = cluster_NN_random_search(cluster_coords, landing_coord)
            total_distance += route_length
            pad_x = int(round(landing_coord[0]))
            pad_y = int(round(landing_coord[1]))

            #NS: Store each drone's information
            coords_to_output = full_path[1:-1]
            node_indices_output = []
            for coord in coords_to_output:
                index = original_indices_map[tuple(coord)]
                node_indices_output.append(str(index))

            output_indices_str = " ".join(node_indices_output)

            solutions.append({
                "landing_coord": (pad_x, pad_y), 
                "num_nodes": len(cluster_coords),
                "route_length": round(route_length, 1),
                "full_path": full_path,
                "output_indices_str": output_indices_str,
                "drone_num": i+1})
            
        all_solutions[k] = solutions
        total_cost = round(total_distance, 1)
        print(f"{k}) If you use {k} drone(s), the total route will be {total_cost} meters")
        prefixes = ["i", "ii", "iii", "iv"]
        for i, soln in enumerate(solutions):
            prefix = prefixes[i]
            landing_pad = soln["landing_coord"]
            print(f"\t{prefix}. Landing Pad {i+1} should be at [{landing_pad[0]}, {landing_pad[1]}], serving {soln["num_nodes"]} locations, route is {soln["route_length"]} meters")

    # drone count decision
    drone_choice = 0
    drone_choices = [1, 2, 3, 4]
    while drone_choice not in drone_choices:
        drone_input = input("Please select your choice 1 to 4: ")
        try:
            drone_choice = int(drone_input)
            if drone_choice not in drone_choices:
                print("Invalid input, please select 1, 2, 3, or 4")
        except:
            print("Invalid input, please enter a number 1 through 4")
            drone_choice = 0
    
    final_solutions = all_solutions[drone_choice]
    WriteSolution(filepath, final_solutions)

# writes the order with the best cost to file according to the 
# output specifications 
def WriteSolution(filepath, solutions):
    splitFile = os.path.splitext(filepath)
    base_name = splitFile[0]
    output_paths = []
    
    # create the txt file outputs
    for solution in solutions:
        drone_id = solution["drone_num"]
        route_cost = int(round(solution["route_length"]))
        output_path = f"{base_name}_{drone_id}_SOLUTION_{route_cost}.txt"
        output_paths.append(output_path)
    
        outputFile = open(output_path, "w")
        outputStr = solution["output_indices_str"]

        outputFile.write(outputStr.strip())
        outputFile.close()

    output_string = "Writing " + ", ".join(output_paths) + " to disk"
    print(output_string)

    return output_paths

# returns array of strings read from filename
def ReadFile(filename):
    file = open(filename, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

# parses IEEE numbers formatted accorded to input specs
# returns (x,y) list of coordinates from file contents
def ParseFile(lines):
    coords_with_index = []
    for i, line in enumerate(lines):
        numbers = line.split("   ")
        while '' in numbers:
            numbers.remove('')
        x = float(numbers[0].strip())
        y = float(numbers[1].strip())
        coord = [x, y]
        coords_with_index.append((coord, i))
    return coords_with_index

# computes the Euclidean distance between 2 coordinates
def EuclideanDistance(coord1, coord2):
    a = pow(coord2[0] - coord1[0], 2)
    b = pow(coord2[1] - coord1[1], 2)
    return math.sqrt(a + b)

#MO: This function computes the nearest neighbor path. 
##   If randomize is True, it will do a nearest neighbor with a random chance of deviation.
def compute_cluster_NN(cluster_coords:list, center_coord:list, randomize:bool):
    nodes_to_visit = list(cluster_coords)
    num_nodes = len(nodes_to_visit)

    nn_path = [center_coord] #NS: Start at cluster center (landing pad)
    visited = set()
    curr_coord = center_coord
    nn_solution = 0.0

    for _ in range(num_nodes):
        first_closest_index = None
        first_closest_dist = float('inf')
        second_closest_index = None
        second_closest_dist = float('inf')
        for j, target_coord in enumerate(nodes_to_visit):
            if j not in visited:
                dist = EuclideanDistance(curr_coord, target_coord)
                if dist < first_closest_dist:
                    second_closest_dist = first_closest_dist
                    second_closest_index = first_closest_index
                    first_closest_index = j
                    first_closest_dist = dist
                elif dist < second_closest_dist:
                    second_closest_dist = dist
                    second_closest_index = j
                    
        if first_closest_index is None:
            break
        if randomize and second_closest_index is not None and random.random() < 0.1:
            closest_index = second_closest_index
            closest_distance = second_closest_dist
        else:
            closest_index = first_closest_index
            closest_distance = first_closest_dist

        next_coord = nodes_to_visit[closest_index]
        visited.add(closest_index)
        nn_path.append(next_coord)
        nn_solution += closest_distance
        curr_coord = next_coord
    
    nn_solution += EuclideanDistance(curr_coord, center_coord) #NS: Add final distance from end node back to center cluster (landing pad)
    nn_path.append(center_coord) #NS: End at cluster center (landing pad)

    return nn_path, nn_solution

#MO: This function performs a nearest neighbor search with random path variation
def cluster_NN_random_search(cluster_coords:list, center_coord:list):
    #MO: Compute NN path
    best_path, best_solution = compute_cluster_NN(cluster_coords, center_coord, False)

    iterations = 0
    while (iterations < 100): #NS: Runs through multiple iterations, no longer anytime algorithm
        random_path, random_solution = compute_cluster_NN(cluster_coords, center_coord, True)
        if random_solution <= best_solution:
            best_solution = random_solution
            best_path = random_path
        iterations += 1

    return best_solution, best_path

#MO: Helper takes in current cluster centers and returns cluster assignments
def classify_nodes(cluster_centers: list, all_coordinates: list):

    if not cluster_centers:
        raise ValueError("cluster_centers must contain at least one center")

    cluster_assignments = []

    for i in range(len(all_coordinates)):
        current_closest_index = None
        current_closest_dist = float("inf")
        for j in range(len(cluster_centers)):
            distance_to_center = math.dist(all_coordinates[i], cluster_centers[j])
            if distance_to_center < current_closest_dist:
                current_closest_dist = distance_to_center
                current_closest_index = j
        cluster_assignments.append(current_closest_index)
    
    return cluster_assignments

#MO: Helper calculates new cluster centers 
def recalculate_clusters(all_coordinates: list, cluster_assignments: list, num_clusters: int):

    #MO: Compute sums of distances
    dist_sums = [[0.0,0.0] for _ in range(num_clusters)] 
    num_assigned = [0] * num_clusters

    for i in range(len(cluster_assignments)):
        dist_sums[cluster_assignments[i]][0] += all_coordinates[i][0]
        dist_sums[cluster_assignments[i]][1] += all_coordinates[i][1]
        num_assigned[cluster_assignments[i]] += 1

    #MO: Get bounds of the coordinates
    if all_coordinates:
        xs = [p[0] for p in all_coordinates]
        ys = [p[1] for p in all_coordinates]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
    else:
        min_x, max_x, min_y, max_y = -10.0, 10.0, -10.0, 10.0
    
    #MO: Calculate cluster centers
    new_centers = []
    for i in range(num_clusters):
        if num_assigned[i] > 0:
            new_centers.append(((dist_sums[i][0] / num_assigned[i]), (dist_sums[i][1] / num_assigned[i])))
        else:
            new_centers.append([random.uniform(min_x, max_x), random.uniform(min_y, max_y)]) 
    
    return new_centers


#MO: Driver function that runs K means algorithm and returns the sets of assignments to run a search on
#TODO: Finish this function
def KMeans_Classify(all_coordinates: list, num_centers: int):
    #Start with random darts
    cluster_centers = [[random.uniform(-10, 10), random.uniform(-10, 10)] for i in range(num_centers)] 
    #Classify nodes by distance to center
    prev_clusters = cluster_centers
    i = 0
    while(i < 100): 
        #Reestimate centers
        cluster_assignments = classify_nodes(cluster_centers, all_coordinates)
        cluster_centers = recalculate_clusters(all_coordinates, cluster_assignments, num_centers)
        #NS: Keep going until centers stop changing or ran too long (100 iterations, need to stop for time constraints)
        if (cluster_centers == prev_clusters):
            break
        prev_clusters = cluster_centers
        i += 1

    #NS: Create library for cluster classifications for each coord
    cluster_data = defaultdict(list)
    for j, coord in enumerate(all_coordinates):
        cluster_index = cluster_assignments[j]
        cluster_data[cluster_index].append(coord)

    return cluster_centers, cluster_data

# writes the order with the best cost to file according to the 
# output specifications 
def WriteSolution(filepath, bestCost, bestOrder):
    splitFile = os.path.splitext(filepath)
    outputPath = splitFile[0] + "_solution_" + str(int(bestCost)) + ".txt"
    
    # create the txt file output
    outputFile = open(outputPath, "w")
    outputStr = ""  
    for index in bestOrder:
        outputStr += str(index + 1) + " "
    outputFile.write(f"{outputStr}")
    outputFile.close()

    return outputPath

# Draws and saves a graph of the solutions to disk
def DrawGraph(file, solutions):
    # set up the plot
    plt.figure(figsize=(19.20, 19.20), dpi=100)
    plt.rcParams.update({'font.size': 22})
    plt.title(f"Best Routes Found Per Cluster", fontsize=32)
    plt.xlabel('X-Axis (Meters)', fontsize=24)
    plt.ylabel('Y-Axis (Meters)', fontsize=24)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.draw()

    # graph each route
    colors = ["#D81B60", "#1E88E5", "#FFC107", "#004D40"]
    for i, sol in enumerate(solutions):
        coordinates = sol[0]
        center = sol[1]
        bestOrder = sol[2]
        x = []
        y = []
        for j in bestOrder:
            x.append(coordinates[j][0])
            y.append(coordinates[j][1])
        plt.plot(x, y, color=colors[i], linewidth=2, marker='o', markersize=10)
        plt.plot(center[0], center[1], color=colors[i], marker='*', markersize=30)
    
    plt.tight_layout()
    plt.grid()
    plt.savefig(file + "_OVERALL_SOLUTION.png", dpi=100)

# produces a simple test graph
def TestDrawGraph():
    coord1 = [(100,100), (300,100), (100,300)]
    center1 = (150,150)
    bestOrder1 = (0,1,2,0)
    sol1 = [coord1, center1, bestOrder1]

    coord2 = [(-600,-200), (-350,-130), (-400,-500)]
    center2 = (-440,-300)
    bestOrder2 = (0,1,2,0)
    sol2 = [coord2, center2, bestOrder2]

    solutions = [sol1, sol2]
    DrawGraph("test", solutions)

#TODO: Use finalized centers and assignments to run the search algorithm to compute paths.

if __name__== "__main__":
    main()
    # filepath = input("Enter the name of the file: ")
    # filename = r"C:\Users\noahj\CS 179M\-MN-2-Software-Solutions-Repo-P1\test\Walnut2621.txt"
    # # read the file
    # coords = []

    # with open(filename, 'r') as file:
    #     for line in file:
    #         x, y = map(float, line.split())
    #         coords.append((x,y))
    #TESTS
    # num_centers = 1
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(f"1 Cluster - ")
    # KMeans_Classify(coords, num_centers)
    # num_centers = 2
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(f"2 Clusters - ")
    # KMeans_Classify(coords, num_centers)
    # num_centers = 3
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(f"3 Clusters - ")
    # KMeans_Classify(coords, num_centers)
    # num_centers = 4
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(f"4 Clusters - ")
    # KMeans_Classify(coords, num_centers)

    # test_nodes = [i for i in range(15)]
    # for i in range(1,5):
    #     assign_num_nodes(len(test_nodes), i)

    # TestDrawGraph()