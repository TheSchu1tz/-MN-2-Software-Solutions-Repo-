import numpy as np
import os
from pathlib import Path
import itertools
import app.components.balance_ship as bs
import time
from queue import PriorityQueue
from app.components.data_types.container import Container

# Node class represents a state in the puzzle and represents the state as a list
class Node:
    def __init__(self, state =None, parent=None, depth = 0, cost=0, g_func = 0):
        if state is None:   # If no state is given, set state to an empty list
            state = []
        elif not isinstance(state, np.ndarray):  # If state is not a numpy array, raise an error
            raise ValueError("State must be a numpy array")
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.g_func = g_func # Accumulating cost of doing this move
        self.h_func = calculate_heuristic(self.state) # Heuristic value of this state
        self.f_func = self.g_func + self.h_func

    def __lt__(self, other):
        return self.f_func < other.f_func

    # Just for hashing purposes
    def map_string(self):
        return str(self.state.flatten())    
    
    # Add possible moves to expanded_nodes
    def expand(self):
        expanded_nodes = []

        # Limit possible moves by limiting which side to move from
        l_weight, r_weight, _, _ = get_side_comparison(self.state)

        if l_weight > r_weight:
             source_cols = range(0, bs.GRID_COLS // 2)
        elif r_weight > l_weight:
             source_cols = range(bs.GRID_COLS // 2, bs.GRID_COLS)
        else:
             source_cols = range(bs.GRID_COLS)

        # Search for all possible containers to move
        movable_containers = []
        for column in source_cols:
            for row in range(bs.GRID_ROWS -1, -1, -1):
                container = self.state[row][column]
                if  container.item != bs.UNUSED and container.item != bs.NAN: # Found a movable container
                    movable_containers.append((row, column))
                    break
        
        #For all movable containers, add all potential moves to expanded nodes
        for container in movable_containers:
            for column in range(bs.GRID_COLS):

                if column == container[1] or self.state[bs.GRID_ROWS - 1][column].item != bs.UNUSED: #Skip same column or full columns
                    continue

                cost, new_state = bs.MoveToColumn(self.state, self.state[container[0]][container[1]], column)

                # Skip adding unreachable nodes
                if cost == float("inf"):
                    continue
                
                expanded_nodes.append(Node(new_state, self, self.depth + 1, cost, self.g_func + cost))
        
        return expanded_nodes

# Helper function for getting the weights of both sides in a state
def get_side_comparison(state:np.ndarray):
        #Get Weights of both sides
        left_weight = 0
        right_weight = 0
        mid_col = bs.GRID_COLS // 2

        for y in range(bs.GRID_ROWS):
            for x in range(bs.GRID_COLS):
                container:Container = state[y][x]
                if container and container.item != bs.UNUSED and container.item != bs.NAN:
                    if x < mid_col:
                        left_weight += container.weight
                    else:
                        right_weight += container.weight
        
        #Figure out who is heavier
        if left_weight > right_weight:
            heavy_cols = range(0, mid_col)     
            light_cols = range(mid_col, bs.GRID_COLS) 
        else:
            heavy_cols = range(mid_col, bs.GRID_COLS)
            light_cols = range(0, mid_col)
    
        return left_weight, right_weight, light_cols, heavy_cols

# Using modified CheckBalance function to calculate the heuristic
def calculate_heuristic(state:np.ndarray):

    if bs.CheckBalance(state): # Edge Case
        return 0
    
    left_weight, right_weight, light_cols, heavy_cols = get_side_comparison(state)
    
    # Search for all movable containers on the heavy side
    from_containers = []
    for column in heavy_cols:
        for row in range(bs.GRID_ROWS -1, -1, -1):
            container = state[row][column]
            if  container.item != bs.UNUSED: 
                if container.item != bs.NAN:
                    from_containers.append(container) # Found a movable container
                    break
                
    
    # Search for all possible columns on light side
    to_cells = []
    for column in light_cols:
        target = -1
        for row in range(bs.GRID_ROWS -1, -1, -1):
            container = state[row][column]
            if  container.item != bs.UNUSED: 
                target = row # Found an empty cell to move the container to
                break
            
        row_placement = target + 1 # Place container ontop of floor
        if row_placement < bs.GRID_ROWS:
            to_cells.append((row_placement, column))
    
    # If these are empty, no possible moves
    if not to_cells or not from_containers:
        return float('inf')
    
    min_h = float('inf')

    for start in from_containers:
        for end_row, end_col in to_cells:
            dist = abs(start.coord.col - end_col) + abs(start.coord.row - end_row)

            if dist < min_h:
                min_h = dist
    # #Get the costs of each available move
    # move_costs = []
    # for start in from_containers:
    #     min_dist = float('inf')
    #     for end_row, end_col in to_cells:
    #         dist = abs(start.coord.col - end_col) + abs(start.coord.row - end_row)

    #         if dist < min_dist:
    #             min_dist = dist
    #     move_costs.append(min_dist)

    # # Grab our weights
    # from_weights = [c.weight for c in from_containers]
    # from_weights.sort(reverse=True)

    # # Calculate how many containers we need to move to reach our goal
    # weight_to_move = 0
    # min_containers_to_move = 0

    # for weight in from_weights:
    #     weight_to_move += weight
    #     min_containers_to_move += 1

    #     new_heavy = max(left_weight, right_weight) - weight_to_move
    #     new_light = min(left_weight, right_weight) + weight_to_move

    #     if abs(new_heavy - new_light) <= (left_weight + right_weight) * 0.10:
    #         break
        
    
    # # Edge case: moving all of the containers will still not be enough to reach the target
    # if min_containers_to_move > len(from_containers):
    #     min_containers_to_move = len(from_containers)

    # # Get the H value by summing up the cost of the cheapest moves using the minimum amount of containers to move
    # move_costs.sort()
    # min_h = sum(move_costs[:min_containers_to_move])
    return min_h
    

# Run the A* search algorithm on a given grid
def run_search(starting_grid: np.ndarray) -> Node:

    start_time = time.time()
    time_limit = 240 # 4 minutes
    wrap_up = False

    tie_breaker = itertools.count() # This is just to break ties in the queue when two heuristic values are the same
    q = PriorityQueue()
    visited = set()

    init_state = Node(starting_grid) # Convert the grid to a Node type

    # Adding deficit to a queue to prioritize useful moves
    l_weight, r_weight, _, _ = get_side_comparison(init_state.state)
    init_deficit = abs(l_weight - r_weight)
    
    # print(f"DEBUG: STARTING WITH INITIAL H VALUE OF {init_state.h_func}")
    q.put((init_state.f_func, init_deficit, next(tie_breaker), init_state)) # Add initial state to the queue with heuristic function

    while(q): # Start searching by popping elements off the queue
        
        # Search has gone on too long time to wrap up using greedy
        if not wrap_up and (time.time() - start_time > time_limit):
            print(f"Time limit reached, solution will not be optimal.")
            wrap_up = True

            #NOTE: This solution is very hacky but we need to speed this up
            with q.mutex:
                all_nodes = list(q.queue) 
                q.queue.clear() # Instantly empty the queue
            
            nodes_only = [item[-1] for item in all_nodes]
            
            nodes_only.sort(key=lambda n: n.h_func)
            
            nodes_only = nodes_only[:50]

            print("Nodes sorted and pruned")
            for node in nodes_only:
                l, r, _, _ = get_side_comparison(node.state)
                deficit = abs(l - r)
                q.put((node.h_func, deficit, next(tie_breaker), node))

            print("Queue reinitialized, using h_func as priority")

        _, _, _, curr_node = q.get()

        if bs.CheckBalance(curr_node.state):
            # print(f"DEBUG: SHIP BALANCED. g = {curr_node.g_func}, h = {curr_node.h_func}")
            return curr_node, len(visited)
        
        # Make sure we don't search the same state twice
        state_id = curr_node.map_string()
        if state_id in visited:
            continue
        visited.add(state_id)
        
        expanded_nodes = curr_node.expand()
        
        for node in expanded_nodes:
            if node.map_string() not in visited:
                l_weight, r_weight, _, _ = get_side_comparison(node.state)
                new_deficit = abs(l_weight - r_weight)
                if wrap_up:
                    q.put((node.h_func, new_deficit, next(tie_breaker), node))
                else:
                    q.put((node.f_func, new_deficit, next(tie_breaker), node))

    # This is an error condition
    print("Cannot reach a solution... exiting")
    return None, None

# This is for testing, comment this out when running the actual program
# if __name__=="__main__":

#     input_files = [
#         "test_manifests/ShipCase1.txt",
#         "test_manifests/ShipCase2.txt",
#         "test_manifests/ShipCase3.txt",
#         "test_manifests/ShipCase4.txt",
#         "test_manifests/ShipCase5.txt",
#         "test_manifests/ShipCase6.txt",
#         "test_manifests/HMM_Algeciras.txt"
#     ]

#     for file in input_files:

#         file_lines = bs.ReadFile(file)

#         manifest = bs.ParseFile(file_lines)

#         begin = time.time()
#         starting_grid = bs.CreateGrid(manifest)

#         final_grid = run_search(starting_grid)
#         end = time.time()

#         p = Path(file)

#         print(f"Took {end - begin} seconds to compute solution for {p}")

#         out_dir = Path("test_solutions")
#         out_dir.mkdir(parents=True, exist_ok=True)

#         with open(out_dir / (p.stem + "_SOLUTION.txt"), "x") as new_file:
#             for container in final_grid.state.flat:
#                 new_file.write(f"[0{container.coord.row + 1},{container.coord.col + 1}], {{{container.weight}}}, {container.item}\n")
    
