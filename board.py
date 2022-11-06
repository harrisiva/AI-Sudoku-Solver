from main import Graph, Variable

# 0's are blank cells (no-assignments)
board = [
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

def get_adjacent(board,i,j): # Return a list of adjacent indexs as tuples, use it for the box perhaps and to create edges
    adjacent = []
    if i!=len(board[0])-1: adjacent.append(f'board[{i+1}][{j}]') # Down (if not last row)
    if i!=0: adjacent.append(f'board[{i-1}][{j}]')  # Up (if not first row)
    if j!=len(board)-1: adjacent.append(f'board[{i}][{j+1}]') # Right (if not right most col)
    if j!=0: adjacent.append(f'board[{i}][{j-1}]') # Left (if not left most col)
    return adjacent

def alldiff(board,i,j): # Given the puzzle and a cell's index, this function returns the all diff as a binary constraint relative to that cell
    given = (i,j)
    constraints = []
    # Get all the other indexs in the same row and column as a tuple
    for x in range(0,len(board),1):
        if x==i: # if row in itteration==i(row of the element), append that entire row
            for y in range(0,len(board[x]),1):
                if (x,y)!=given: constraints.append(f'board[{i}][{j}]!=board[{x}][{y}]')
        if (x,j)!=given: constraints.append(f'board[{i}][{j}]!=board[{x}][{j}]') 
    return constraints

def get_constraints(board,i,j):
    constraints = alldiff(board,i,j)
    return constraints

def sudokuGraphify(board:list)->Graph:
    sudokuDomain = [1,2,3,4,5,6,7,8,9]
    graph = Graph()
    # convert the board to a graph loop through each index pair and get adjacent and add it as a edge
    for i in range(0,len(board),1):
        for j in range(0,len(board),1):
            constraints = get_constraints(board,i,j) # generate all the constraints for the current (from) node (i,j)
            adjacent = get_adjacent(board,i,j)
            for cell in adjacent:
                from_node = Variable(f'board[{i}][{j}]',board[i][j],sudokuDomain)
                to_node = Variable(cell,eval(cell),sudokuDomain)
                graph.add_edge(from_node,to_node,constraints)
    return graph


# Contains the correct amount of nodes
# Contains the correct amount of direct edges
# Contains the current alldiff binarized constraints
# Mising the box constraints
graph: Graph = sudokuGraphify(board)