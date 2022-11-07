# MODEL 2


# simpler DS:
domains = {} # variable domain dictionary
assignments = {} # assignment dictionary
constaints = {} # variable constraint dictionary

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

INITIAL_DOMAIN = [1,2,3,4,5,6,7,8,9]


# to view, just map the assignment dictionary to a matrix (have map as a separate dictionary)
# for values not in the assignemnt dictionary, just leave a zero in place 

# for ac-3
# take a vairbale that is not in the assignment dictionary
# trim its domain based on the constraint dictionary
# if a domain is every zero, remove it


# for backtracking, rather than taking instances of ds's, we just take the dictionaries
