from constants import *
from classes import Graph, Variable, CSP
from utilities import sudokuGraphify
from functions import ac3
import numpy as np # Only used to view the sudoku board

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
        #print(csp)
        for node in csp.graph.nodes:
            node:Variable = node
            if len(node.domain)==1:
                board[node.i][node.j] = node.domain[0]
        print(np.array(board))