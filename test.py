from constants import *
# columns are mapped as j-1

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

domains = {}
assignments = {}
constraints = {}

INITIAL_STANDARD_DOMAIN = [1,2,3,4,5,6,7,8,9]
for i in range(0,len(board),1):
    for j in range(0,len(board[i]),1):
        name = f'{ROW_INDEX_AS_KEY[i]}{j+1}' # j+1 because we are mapping 0 index as 1
        domain = INITIAL_STANDARD_DOMAIN if board[i][j]==0 else [board[i][j]]
        value = board[i][j]
        
        domains[name]=domain
        assignments[name]=value

print(domains)
print(assignments)

# to create variable name and map
# i number = letter
# j is preserved 



# convert old constraints using maping functions and load all constraints onto a file