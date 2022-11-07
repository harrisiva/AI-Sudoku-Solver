from constants import *
from classes import Graph, Variable, CSP
from utilities import sudokuGraphify
from functions import ac3
import numpy as np # Only used to view the sudoku board
import copy

#NOTE: ADD PREMATURE INPUT CHECKS

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

        def is_consistent(assignment,variable, value, csp, given_board):
            # original copy of board, the changes are done on this to preserve reference related issues
            board = copy.deepcopy(given_board)

            # find one of the edges where this variable is a from node
            # get a copy of the constraints
            constraints = None
            for edge in csp.graph.edges:
                if edge[0].name == variable.name:
                    constraints = edge[2]
                    break

            # set this value as the variables value in the board
            board[variable.i][variable.j]=value

            modified_nodes = []
            modified_values = []
            # set all the variable value pairs in the assignment list as cell values
            if len(assignment)>0:
                for var in assignment: 
                    for node in csp.graph.nodes:
                        if node.name==var:
                            modified_nodes.append(node) # NOTE: Loop at the end, and set value back to zero (assuming zero is the original)
                            modified_values.append(node.value)
                            node.value=assignment[var] # NOTE: Need to reset at the end
                            board[node.i][node.j]=node.value 
            # check if the variable is still consistent (relative to the board)
            consistent = True
            for constraint in constraints: consistent=False if eval(constraint)==False else consistent

            # Reset the assignment variables back to their original value
            for i in range(0,len(modified_nodes),1): modified_nodes[i].value=modified_values[i]

            # reset the board to its original state NOTE: Not required as all changes are made on the deepcopy of the board
            return consistent

        def backtrack(assignment,csp, board):
            print(assignment)
            if is_complete(assignment,csp): return assignment
            variable:Variable = selected_unassigned_variable(csp) # uses the MRV heuristic
            
            for value in variable.domain:
                # check if value is consistent with assignment
                if is_consistent(assignment,variable, value, csp, board):
                    
                    board_copy = copy.deepcopy(board)
                    
                     # keep a copy domains pre trim (inference)
                    pre_infrences = {}
                    for node in csp.graph.nodes: pre_infrences[node.name]=copy.deepcopy(node.domain)

                    # Add variable to the assignment
                    assignment[variable.name]=value # add the variable value pair to the assignments dictionary
                    variable.value = value # assign the value to the variable
                    board[variable.i][variable.j]=variable.value # update the board to hold the assignment
                    # update the constraints for all from_node.name==variable.name nodes:
                    # if variable.value!=0, append constraint variable.name==variable.value
                    for edge in csp.graph.edges:
                        if edge[0].name==variable.name: edge[2].append(f'board[{variable.i}][{variable.j}]=={variable.value}')
                    

                    # Get infrences
                    infered = ac3(csp,board)
                    if infered!=False:

                        # add the inferences to assignment by updating the variables and board to hold the single length domain values
                        for node in csp.graph.nodes:
                            if len(node.domain)==1:
                                node.value = node.domain[0]
                                board[node.i][node.j]=node.value
                        
                        print(np.array(board))
                        result = backtrack(assignment,csp,board)

                        if isinstance(result,dict):
                            return result

                    # remove var and its value and infrences from assignment 
                    del assignment[variable.name]
                    variable.value = 0
                    board[variable.i][variable.j]=0
                    
                    # remove infrences from assignment by reseting the board to the state before we called AC-3 and resetting the domain of the changed variables
                    board = copy.deepcopy(board_copy)
                    for node in csp.graph.nodes: node.domain = copy.deepcopy(pre_infrences[node.name])
            
            return False
    
        def backtracking_search(csp, board):
            assignment = {}
            return backtrack(assignment,csp, board)
        
        backtracking_search(csp, board)
        #NOTE: Constraints include constraints not starting from the current node (this is wrong, need to fix the part where the constraints are loaded in)


