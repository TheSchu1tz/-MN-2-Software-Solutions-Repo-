import math
import random
import os
import matplotlib.pyplot as plt
from collections import defaultdict


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
    for i in range(num_centers):
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
    print(f"Initial: {cluster_centers}")
    i = 0
    while(i < 10): 
        #Reestimate centers
        cluster_assignements = classify_nodes(cluster_centers, all_coordinates)
        cluster_centers = recalculate_clusters(all_coordinates, cluster_assignements, num_centers)
        #Keep going until centers stop changing
        print(f"\tNew: {cluster_centers}")
        i += 1
    return

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
    # filepath = input("Enter the name of the file: ")
    filename = "test/Walnut2621.txt"
    # read the file
    coords = []

    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.split())
            coords.append((x,y))
    #TESTS
    # num_centers = 1
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(classify_nodes(cluster_centers, coords))
    # num_centers = 2
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(classify_nodes(cluster_centers, coords))
    # num_centers = 3
    # cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    # print(classify_nodes(cluster_centers, coords))
    num_centers = 3
    cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    KMeans_Classify(coords, num_centers)
    # test_nodes = [i for i in range(15)]
    # for i in range(1,5):
    #     assign_num_nodes(len(test_nodes), i)

    # TestDrawGraph()