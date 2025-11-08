import math
import random
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
