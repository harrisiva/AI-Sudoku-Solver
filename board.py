from main import Graph, Variable

# 0's are blank cells
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

sudokuDomain = [1,2,3,4,5,6,7,8,9]
graph = Graph()
# convert the board to a graph loop through each index pair and get adjacent and add it as a edge
for i in range(0,len(board),1):
    for j in range(0,len(board),1):
        adjacent = get_adjacent(board,i,j)
        for cell in adjacent:
            from_node = Variable(f'board[{i}][{j}]',board[i][j],sudokuDomain)
            to_node = Variable(f'{cell}',eval(cell),sudokuDomain)
            # generate all the constraints for the 'from_node'
            graph.add_edge(from_node,to_node,[])