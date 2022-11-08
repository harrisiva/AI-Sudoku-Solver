from constants import *
# MODEL 2

board = [
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

def loadSudoku(board):
    variables = []
    indexes = {}
    domains = {}
    assignments = {}
    constraints = {}

    with open('map_constraints.txt','r') as file: BOXCONSTRAINTS=[line.replace('\n','') for line in file.readlines()] # Load box constraints from map_constraints file
    for i in range(0,len(board),1):
        for j in range(0,len(board[i]),1):
            name = f'{ROW_INDEX_AS_KEY[i]}{j+1}' # j+1 because we are mapping 0 index as 1
            domain = INITIAL_STANDARD_DOMAIN if board[i][j]==0 else [board[i][j]]
            value = board[i][j]
            constraints_list = []
            
            # Generate the alldiff constraints for this variable
            for row in range(len(board)):
                for col in range(len(board[row])):
                    if row == i and col!=j:
                        constraints_list.append(f'{name}!={ROW_INDEX_AS_KEY[row]}{col+1}')
                    if col == j and row != i:
                        constraints_list.append(f'{name}!={ROW_INDEX_AS_KEY[row]}{col+1}')

            # Retrive the box constraints for this variable (where this variable is the from node)
            for constraint in BOXCONSTRAINTS: 
                if name in constraint[:2]: constraints_list.append(constraint)

            variables.append(name)
            indexes[name]=[i,j]
            domains[name]=domain
            if value!=0: assignments[name]=value # NOTE: Append variable:value only if variable has a value assigned to it (meaning !=0 since 0's are blank)
            constraints[name]=constraints_list

    return variables, indexes, domains, assignments, constraints

variables, indexes, domains, assignments, constraints = loadSudoku(board)

# for ac-3
# take a vairbale that is not in the assignment dictionary
# trim its domain based on the constraint dictionary
# if a domain is every zero, remove it


# for backtracking, rather than taking instances of ds's, we just take the dictionaries
