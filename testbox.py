from constants import *

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
    with open("map_constraints.txt","a+") as f:
        for i in range(x, y):
            for j in range(w, z):
                for k in range(x,y):
                    for l in range(w, z):
                        if (k,l) != (i, j):
                            #temp = f'board[{i}][{j}]!=board[{k}][{l}]'
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