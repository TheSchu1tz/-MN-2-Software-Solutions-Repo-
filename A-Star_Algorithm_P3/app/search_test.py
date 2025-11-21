import numpy as np
import components.balance_ship as bs
from queue import PriorityQueue

# Node class represents a state in the puzzle and represents the state as a list
class Node:
    def __init__(self, state =None, parent=None, depth = 0, cost=0):
        if state is None:   # If no state is given, set state to an empty list
            state = []
        elif not isinstance(state, np.ndarray):  # If state is not a numpy array, raise an error
            raise ValueError("State must be a numpy array")
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
    
    # Add possible moves to expanded_nodes
    def expand(self):
        expanded_nodes = []

        # Search for all possible containers to move
        movable_containers = []
        for column in range(bs.GRID_COLS):
            for row in range(bs.GRID_ROWS):
                if self.state[row][column] != bs.UNUSED and self.state[row][column] != bs.NAN: # Found a movable container
                    movable_containers.append((row, column))
        
        #For all movable containers, add all potential moves to expanded nodes
        for container in movable_containers:
            for column in range(bs.GRID_COLS):
                cost, new_state = bs.MoveToColumn(self.state, self.state[container[0]][container[1]], column)
                expanded_nodes.append((cost, Node(new_state, self.state, self.depth + 1, cost)))

                    
            

# Run the A* search algorithm on a given grid
def run_search(starting_grid: np.ndarray):

    q = PriorityQueue()
    init_state = Node(starting_grid) # Convert the grid to a Node type
    q.put((0, init_state)) # Add initial state to the queue with cost 0

    while(q): # Start searching by popping elements off the queue
        curr_node = q.get()
        if bs.CheckBalance(curr_node.state):
            return curr_node.state
        expanded_nodes = curr_node.expand()
        for cost, node in expanded_nodes:
            q.put((cost, node))

    return None

if __name__=="__main__":

    input_file = "test_manifests/ShipCase3.txt"

    file_lines = bs.ReadFile(input_file)

    manifest = bs.ParseFile(file_lines)

    starting_grid = bs.CreateGrid(manifest)

    
