from classes import Graph, Variable
from constants import *

def gen_box_constraints_helper(x, y, w, z):
    with open("constraints.txt","w") as f:
        for i in range(x, y):
            for j in range(w, z):
                for k in range(x,y):
                    for l in range(w, z):
                        if (k,l) != (i, j):
                            temp = f'board[{i}][{j}]!=board[{k}][{l}]'
                            f.write(f'{temp}\n')

def gen_box_constraints():
    gen_box_constraints_helper(0,3, 0,3)
    gen_box_constraints_helper(0,3, 3,6)
    gen_box_constraints_helper(0,3, 6,9)
    gen_box_constraints_helper(3,6, 0,3)
    gen_box_constraints_helper(3,6, 3,6)
    gen_box_constraints_helper(3,6, 6,9)
    gen_box_constraints_helper(6,9, 0,3)
    gen_box_constraints_helper(6,9, 3,6)
    gen_box_constraints_helper(6,9, 6,9)
    return

def get_adjacent(board,i,j): # Return a list of adjacent indexs as tuples, use it for the box perhaps and to create edges
    adjacent = []
    if i!=len(board[0])-1: adjacent.append([f'board[{i+1}][{j}]',i+1,j]) # Down (if not last row)
    if i!=0: adjacent.append([f'board[{i-1}][{j}]',i-1,j])  # Up (if not first row)
    if j!=len(board)-1: adjacent.append([f'board[{i}][{j+1}]',i,j+1]) # Right (if not right most col)
    if j!=0: adjacent.append([f'board[{i}][{j-1}]',i,j-1]) # Left (if not left most col)
    return adjacent

def get_alldiff_constraints(board,i,j): # Given the puzzle and a cell's index, this function returns the all diff as a binary constraint relative to that cell
    given = (i,j)
    constraints = []
    # Get all the other indexs in the same row and column as a tuple
    for x in range(0,len(board),1):
        if x==i: # if row in itteration==i(row of the element), append that entire row
            for y in range(0,len(board[x]),1):
                if (x,y)!=given: constraints.append(f'board[{i}][{j}]!=board[{x}][{y}]')
        if (x,j)!=given: constraints.append(f'board[{i}][{j}]!=board[{x}][{j}]') 
    return constraints

def get_box_constraints(i,j):
    # Load the box constratins from constraints.txt
    with open('constraints.txt','r') as file: lines=[line.replace('\n','') for line in file.readlines()]
    return [line for line in lines if f'board[{i}][{j}]' in line] 

def get_constraints(board,i,j):
    constraints = []
    all_diff_constraints = get_alldiff_constraints(board,i,j)
    for line in all_diff_constraints: constraints.append(line)
    box_constraints = get_box_constraints(i,j)
    for line in box_constraints: constraints.append(line)
    return constraints

def sudokuGraphify(board:list)->Graph:
    graph = Graph() # Initialize a graph object, the board will be "moved" to this
    # Nested for loop to convert the board to a graph
    for i in range(0,len(board),1):
        for j in range(0,len(board),1):

            # Get the constraints related to the current node (nested list based)
            constraints = get_constraints(board,i,j) # generate all the constraints for the current (from) node (i,j)
            if board[i][j]!=0: constraints.append(f'board[{i}][{j}]=={board[i][j]}') # If the node has a value, add it to the constraints list as board[i][j]==value

            # Create a from_node, to_node (based on the adjacent list retrvied from the function called in the line below), and add both to the edge list with the list of constraints
            adjacent = get_adjacent(board,i,j) # Get a list of adjacent cells (index based)
            for cell in adjacent:
                from_node = Variable(f'board[{i}][{j}]',i,j,board[i][j],SUDOKUDOMAIN if board[i][j]==0 else [board[i][j]]) # Last field to make sure that the domain for assigned variables is limited to the value assigned to it alone
                to_node = Variable(cell[0],cell[1],cell[2],eval(cell[0]),SUDOKUDOMAIN if board[cell[1]][cell[2]]==0 else board[cell[1]][cell[2]])
                graph.add_edge(from_node,to_node,constraints)
    return graph