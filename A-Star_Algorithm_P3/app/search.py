import numpy as np
import os
from pathlib import Path
import itertools
import components.balance_ship as bs
from queue import PriorityQueue
from components.data_types.container import Container

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

        # Search for all possible containers to move
        movable_containers = []
        for column in range(bs.GRID_COLS):
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
                
                expanded_nodes.append(Node(new_state, self, self.depth + 1, cost, self.g_func + cost))
        
        return expanded_nodes

                    
            
# Using modified CheckBalance function to calculate the heuristic
def calculate_heuristic(state:np.ndarray):

    if bs.CheckBalance(state): # Edge Case
        return 0
    
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

    min_h = float('inf') 
    
    # Search for all movable containers on the heavy side
    from_columns = []
    for column in heavy_cols:
        for row in range(bs.GRID_ROWS -1, -1, -1):
            container = state[row][column]
            if  container.item != bs.UNUSED: 
                if container.item != bs.NAN:
                    from_columns.append(column) # Found a movable container
                break
    
    # Search for all possible columns on light side
    to_columns = []
    for column in light_cols:
        if state[bs.GRID_ROWS - 1][column].item == bs.UNUSED:
            to_columns.append(column)
    
    #Get the heuristic value
    for start in from_columns:
        for end in to_columns:
            dist = abs(start - end)
            if dist < min_h:
                min_h = dist
    return min_h
    

# Run the A* search algorithm on a given grid
def run_search(starting_grid: np.ndarray):

    tie_breaker = itertools.count() # This is just to break ties in the queue when two heuristic values are the same
    q = PriorityQueue()
    visited = set()

    init_state = Node(starting_grid) # Convert the grid to a Node type
    
    # print(f"DEBUG: STARTING WITH INITIAL H VALUE OF {init_state.h_func}")
    q.put((init_state.f_func, next(tie_breaker), init_state)) # Add initial state to the queue with heuristic function

    while(q): # Start searching by popping elements off the queue
        _, _, curr_node = q.get()

        if bs.CheckBalance(curr_node.state):
            # print(f"DEBUG: SHIP BALANCED. g = {curr_node.g_func}, h = {curr_node.h_func}")
            return curr_node.state
        
        # Make sure we don't search the same state twice
        state_id = curr_node.map_string()
        if state_id in visited:
            continue
        visited.add(state_id)
        
        expanded_nodes = curr_node.expand()
        
        for node in expanded_nodes:
            if node.map_string() not in visited:
                q.put((node.f_func, next(tie_breaker), node))

    # This is an error condition
    return None


# This is for testing, comment this out when running the actual program
if __name__=="__main__":

    input_files = [
        "test_manifests/ShipCase1.txt",
        "test_manifests/ShipCase2.txt",
        "test_manifests/ShipCase3.txt",
        "test_manifests/ShipCase4.txt",
        "test_manifests/ShipCase5.txt",
        "test_manifests/ShipCase6.txt"
    ]

    for file in input_files:

        file_lines = bs.ReadFile(file)

        manifest = bs.ParseFile(file_lines)

        starting_grid = bs.CreateGrid(manifest)

        final_grid = run_search(starting_grid)

        p = Path(file)

        out_dir = Path("test_solutions")
        out_dir.mkdir(parents=True, exist_ok=True)

        with open(out_dir / (p.stem + "_SOLUTION.txt"), "x") as new_file:
            for container in final_grid.flat:
                new_file.write(f"[0{container.coord.row + 1},{container.coord.col + 1}], {{{container.weight}}}, {container.item}\n")
    
