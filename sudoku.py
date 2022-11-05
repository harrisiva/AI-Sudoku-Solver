from main import Graph, Variable
import numpy as np
# Attempting to convert the sudoku puzzle to a graph that can have ac-3 imposed on it

# Each cell in the puzzle is a node
# Each cell can have a maximum of 4 neighbors (2 row, 2 column)
# Constraints include (alldiff rows, columsn)
# also includes (alldiff box) <- harder to structure (do this first, and then branch out)

# Just do it for four nodes first and then scale up

# Can you do it without converting it to a graph?
# Constraints are identified by for loops for rows and cols
# Constraints are also identified using offset math for the box constraint

# Attempting to see if we can get all constraints for each variable as a cell

puzzle = [[0,1,2],[3,4,5],[6,7,8]]

def get_adjacent(puzzle,i,j): # Return a list of adjacent indexs as tuples, use it for the box perhaps and to create edges
    adjacent = []
    if i!=len(puzzle[0])-1: adjacent.append((i+1,j)) # Down (if not last row)
    if i!=0: adjacent.append((i-1,j))  # Up (if not first row)
    if j!=len(puzzle)-1: adjacent.append((i,j+1)) # Right (if not right most col)
    if j!=0: adjacent.append((i,j-1)) # Left (if not left most col)
    return adjacent

adjacent = get_adjacent(puzzle,0,2)

def alldiff(puzzle,i,j): # Given the puzzle and a cell's index, this function returns the all diff as a binary constraint relative to that cell
    given = (i,j)
    row = []
    col = []
    # Get all the other indexs in the same row and column as a tuple
    for x in range(0,len(puzzle),1):
        if x==i: # if row in itteration==i(row of the element), append that entire row
            for y in range(0,len(puzzle[x]),1):
                if (x,y)!=given: row.append(f'{(i,j)}!={(x,y)}')
        if (x,j)!=given: col.append(f'{(i,j)}!={(x,j)}') 
    return row,col

alldiff(puzzle,1,1)
print(puzzle)