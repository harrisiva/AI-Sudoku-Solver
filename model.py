from constants import *
from copy import deepcopy as value
# MODEL 2

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
            assignments[name]=value #if value!=0: assignments[name]=value # NOTE: Append variable:value only if variable has a value assigned to it (meaning !=0 since 0's are blank)
            constraints[name]=constraints_list

    return variables, indexes, domains, assignments, constraints


def evaluate_constraint(constraint:str,assignments:dict):
    return assignments[constraint[0:2]]!=assignments[constraint[4:]]

# revise given the variable_name, domain, and assignment
def revise(variable_name, domains, constraints, assignments):
    variable_domain = value(domains[variable_name]) 
    variable_constraints = constraints[variable_name]
    original_variable_value = value(assignments[variable_name])

    revised = False
    for domain_value in variable_domain: # iterate through this variables domain
        assignments[variable_name]=domain_value # set the current value in iteration as the assignment (value for the variable)
        for constraint in variable_constraints: # loop through the constraints
            if evaluate_constraint(constraint, assignments)==False: # evaluate the constraint
                if domain_value in domains[variable_name]: 
                    domains[variable_name].remove(domain_value) # remove assignment value from the domain's clone (to not break the loop)
                    revised = True

    # Reset the assignment to hold the variables original value
    assignments[variable_name]=original_variable_value
    return revised

# load every variable to the queue 
def ac3(variables,domains,assignments,constraints):
    queue = [variable for variable in variables] # load all variables to a queue
    while len(queue)>=1: # while the queue is not empty 
        variable = queue.pop() # pop a variable from the queue
        revise(variable,domains,constraints,assignments) # revise (trim) the variables domain
        if len(domains[variable])==0: return False # if the variable's domain is trimmed to contain no elements, return False as a solution is not possible
    return True

variables, indexes, domains, assignments, constraints = loadSudoku(solveableBoard)
for variable in variables:
    print(variable,domains[variable])
made_consistent = ac3(variables,domains, assignments, constraints)
print('Made Consistent',made_consistent)
for variable in variables:
    print(variable,domains[variable])


# for backtracking, rather than taking instances of ds's, we just take the dictionaries
