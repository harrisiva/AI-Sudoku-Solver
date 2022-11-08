from constants import *
from copy import deepcopy as asvalue
# MODEL 2

def gen_box_constraints():
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
    def gen_box_constraints_helper(x, y, w, z):
        with open("map_constraints2.txt","a+") as f:
            for i in range(x, y):
                for j in range(w, z):
                    for k in range(x,y):
                        for l in range(w, z):
                            if (k,l) != (i, j):
                                f.write(f'{ROW_INDEX_AS_KEY[i]}{j+1}!={ROW_INDEX_AS_KEY[k]}{l+1}\n')

    gen_box_constraints_helper(0,3, 0,3)
    gen_box_constraints_helper(0,3, 3,6)
    gen_box_constraints_helper(0,3, 6,9)
    gen_box_constraints_helper(3,6, 0,3)
    gen_box_constraints_helper(3,6, 3,6)
    gen_box_constraints_helper(3,6, 6,9)
    gen_box_constraints_helper(6,9, 0,3)
    gen_box_constraints_helper(6,9, 3,6)
    gen_box_constraints_helper(6,9, 6,9)

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
            domain = asvalue(INITIAL_STANDARD_DOMAIN) if board[i][j]==0 else [board[i][j]]
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

# Revise given the variable_name, domain, and assignment
def revise(variable_name, domains, constraints, assignments):
    variable_domain = asvalue(domains[variable_name])
    variable_constraints = constraints[variable_name]
    original_variable_value = asvalue(assignments[variable_name])

    revised = False
    for domain_value in variable_domain: # iterate through this variables domain
        assignments[variable_name]=domain_value # set the current value in iteration as the assignment (value for the variable)
        for constraint in variable_constraints:
            if evaluate_constraint(constraint,assignments)==False: # if it is ever false
                if domain_value in domains[variable_name]: domains[variable_name].remove(domain_value)
                revised = True

    # Reset the assignment to hold the variables original value
    assignments[variable_name]=original_variable_value
    return revised

# Call revise to trim the domain of every variable
def ac3(variables,domains,assignments,constraints):
    for variable in variables:
        revise(variable,domains,constraints,assignments)
        if len(domains[variable])==0: return False
    return True

variables, indexes, domains, assignments, constraints = loadSudoku(AC3_UNSOLVABLE_BOARD)
if ac3(variables,domains,assignments,constraints):
    
    # Update assignments so that variables that have a len(domain)==1 have a value assigned to them. Also determine if solved
    solved = True
    for variable in variables:
        if len(domains[variable])==1: assignments[variable] = domains[variable][0]
        else: solved=False

    print(f'Solved with AC-3 alone:{solved}')
    

    if solved==False:
        print("Executing backtracking with AC-3 as the inference")

        # Utility functions for backtracking
        def is_complete(assignments): # Check if every variable has an assignment (the dictionary has a default value of 0 for each assignment)
            for assignment in assignments: 
                if assignments[assignment]==0: return False
            return True

        def select_unassigned_variable(variables, domains): # For selecting an unassigned variable using the MRV heuristic
            minimum = 9 # Domains can have a max of 8 values
            mrv_variable = None # Initialize mrv_variable as None
            for variable in variables: # Loop through the list of variables
                if len(domains[variable])!=1 and len(domains[variable])<minimum: # if the vairable has a domain greater than 1 and smaller than the minimum
                    minimum = len(domains[variable]) # set the length of the variables domain as the minimum (length of the smallest domain <- updated every iteration)
                    mrv_variable = variable # set the variable as the MRV variable
            return mrv_variable

        def is_consistent(variable,value,assignments,constraints): # Adds the assignment to copy (as value) of the assignments dictionary and checks if all the constraints hold true, if not, returns false, else returns true
            # set the variables value in assignments (copy as value) to be the given value
            assignments_copy:dict = asvalue(assignments) # All changes as made on this (as its a copy by value), not the original assignments dictionary
            assignments_copy[variable]=value
            # check if it is consistent with the cosntraints with the help of the evalute constraint function
            for constraint in constraints[variable]:
                if evaluate_constraint(constraint,assignments_copy)==False: return False
            return True

        
        for variable in variables:
            print(f'{variable}:{domains[variable]}')

        # For backtracking, rather than taking instances of ds's, we just take the dictionaries
        def backtrack(variables,domains,assignments,constraints): # def backtrack(the four variables without the indexes)
            if is_complete(assignments): return assignments
            variable = select_unassigned_variable(variables, domains) # select unassigned variable with the MRV heuristic
            for value in domains[variable]: # for each value in the selected variables domain
                # check if the value is consistent with the current assignments
                if is_consistent(variable,value,assignments,constraints):
                    assignments[variable]=value # add var=value to the assignment
                    # pre_inference = domains
                    infered = ac3(variables,domains,assignments,constraints)
                    # inferences (boolean) <- AC3 (four variables) requirement: needs the unassigned variables to have an assignment as 0 in the dictionary
                    # if inferences did not fail
                        # add infereces to assignment (update assignment to have the domains)
                            # go through the domains that are trimmed to 1
                            # if they are not in the assignment
                            # update them (keep a list?)
                            # return assignmnent (result)
                # remove variable=value (reset to original value) and inferences (reset domains and set the non single length domains as 0 to represent unassigned status) from the assignment 
            # return failure (dictionary with an empty -1 as status)
        

        # def backtrack_search(csp<-the four variables without the indexes)
            # remove all unassigned values from the assignment dictionary and pass this as the assignment instead
            # also pass in sorted MRV list into the backtrack algorithm
else:
    print("Puzzle state is unsolvable")