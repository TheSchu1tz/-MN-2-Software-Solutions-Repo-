import math
import random
from collections import defaultdict

# # Ignore MO: Helper assigns a number of nodes to classify for each cluster center in a list. 
# def assign_num_nodes(num_nodes: int, num_centers: int):
#     #Calculate how many nodes each center will classify
#     nodes_per_center = num_nodes // num_centers
#     remainder_nodes = num_nodes % num_centers

#     assigned_nodes = [nodes_per_center] * num_centers

#     if remainder_nodes != 0: #Case if we cannot evenly distribute nodes
#         i = 0
#         while i < remainder_nodes :
#             assigned_nodes[i % num_centers] += 1
#             i += 1
    
#     return assigned_nodes

#MO: Helper takes in current cluster centers and calculates the updated ones with KNN
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




def KNN_Classify(all_coordinates: list, num_centers: int):
    #Start with random darts
    cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for i in range(num_centers)] 
    #Initialize center coordinates on the map
    #Find KNN for each center
    #Reestimate centers
    #Keep going until centers stop changing
    return

if __name__== "__main__":
    # filepath = input("Enter the name of the file: ")
    filename = "test/pecan1212.txt"
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
    num_centers = 4
    cluster_centers = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(num_centers)] 
    print(classify_nodes(cluster_centers, coords))
    # test_nodes = [i for i in range(15)]
    # for i in range(1,5):
    #     assign_num_nodes(len(test_nodes), i)
