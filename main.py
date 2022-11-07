from constants import *
from classes import Graph, Variable, CSP
from utilities import sudokuGraphify
from functions import ac3
import numpy as np # Only used to view the sudoku board
import copy

if __name__=='__main__':
    # 0's are blank cells (no-assignments)
    solveableBoard = [
        [4,8,3, 9,2,1, 6,5,7],
        [9,6,0, 3,4,5, 8,0,1],
        [2,5,1, 8,7,6, 4,9,3],

        [5,4,8, 1,3,2, 9,7,6],
        [7,2,9, 5,0,0, 1,3,8],
        [1,0,6, 7,9,8, 2,0,5],

        [3,7,2, 6,8,9, 5,1,4],
        [0,1,0, 2,5,3, 7,6,9],
        [6,9,5, 4,1,7, 0,8,2],
    ]
    unsolvableBoard = [
        [0,0,3, 0,2,0, 6,0,0],
        [9,0,0, 3,0,5, 0,0,1],
        [0,0,1, 8,0,6, 4,0,0],

        [0,0,8, 1,0,2, 9,0,0],
        [7,0,0, 0,0,0, 0,0,8],
        [0,0,6, 7,0,8, 2,0,0],

        [0,0,2, 6,0,9, 5,0,0],
        [8,0,0, 2,0,3, 0,0,9],
        [0,0,5, 0,1,0, 3,0,0],
    ]
    
    board = unsolvableBoard
    # Set up CSP
    graph: Graph = sudokuGraphify(board) # Convert the board into a graph
    csp = CSP(graph) # Initialize an instance of CSP with the graph
    for node in graph.nodes: csp.variables.append(node) # Append graph's nodes to the CSP instances variables list
    csp.domain = SUDOKUDOMAIN # set the global domain list as the CSP instances domain
    # Call AC-3 with the CSP
    if ac3(csp,board): 
        for node in csp.graph.nodes:
            node:Variable = node
            if len(node.domain)==1: # If any nodes domain is trimmed to 1
                # Set this in the board (to update the board for constraint verification)
                board[node.i][node.j] = node.domain[0] 
                # Set this as the nodes value (for selecting unassigned MRV's)
                node.value = node.domain[0]
        print(np.array(board))

        # Once a board is deemed to be unsolveable with AC-3 alone 
        # If any domain len>1

        # Run a backtracking search algorithm with AC-3 as the inference
        assignment = {}

        def selected_unassigned_variable(csp:CSP): # returns a list of MRV based nodes using insort (NOTE: insort not implemented yet, it iterates and finds MRV each time currently)
            # Choose a variable without assignment (node.value==0)
            # if the node.value == 0 (i.e., len(node.domain)>1)
            # choose the node with the smallest domain (miniming remaining values)
            graph: Graph = csp.graph
            minimum = 9 # extrema max (no node/cell can have more than 8 values)
            mrv_node = None # holder for the node with minimum remaning values
            for node in graph.nodes:
                node:Variable = node
                if node.value==0:
                    node_domain_length = len(node.domain)
                    if node_domain_length<minimum:
                        minimum = node_domain_length
                        mrv_node = node
            return mrv_node

        def is_complete(assignment:dict, csp:CSP):
            # Check if every node in the CSP!=0 (depending on how we handle rest of backtracking)
            # Check if every node in the CSP!=0 or has an assignment in the dictionary by key
            for node in csp.graph.nodes:
                if (node.value==0) and (node.name not in assignment.values()): return False
            return True

        def is_consistent(assignment,variable, value, csp, board):
            # original copy of board for resetting
            original_board = copy.deepcopy(board)

            # find one of the edges where this variable is a from node
            # get a copy of the constraints
            constraints = None
            for edge in csp.graph.edges:
                if edge[0].name == variable.name:
                    print(edge[0].name)
                    break
            print(constraints)
            if constraints==None: return False # never the case (just here for fun, delete later)

            # set this value as the variables value in the board
            board[variable.i][variable.j]=value
            print (board)
            board = original_board
            # set all the variable value pairs in the assignment list as assignments
            for var in assignment: pass
                

            # check if the variable is still consistent (relative to the board)
            # set the consistency boolean based on the latter
            # reset the board to its original state
            # return the consistency boolean value
            return 

        def backtrack(assignment,csp, board):
            if is_complete(assignment,csp): return assignment
            variable:Variable = selected_unassigned_variable(csp) # uses the MRV heuristic
            for value in variable.domain:
                # check if value is consistent with assignment
                print(value, is_consistent(assignment,variable, value, csp, board))
                pass
            return
    
        def backtracking_search(csp, board):
            assignment = {}
            return backtrack(assignment,csp, board)
        
        backtracking_search(csp, board)
        #NOTE: Constraints include constraints not starting from the current node (this is wrong, need to fix the part where the constraints are loaded in)