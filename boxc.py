puzzle = [
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],

    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],

    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0]
]

# col pairs:
    # 0 to 2
    # 3 to 5
    # 6 to 8

# row pairs
    # same as col pairs

constraints = []

# Get indexes of box and then pair all of them with each other

# getting indexes of the box
for i in range(0,len(puzzle),1):
    print(i,i%3)
    for j in range(0,len(puzzle[i]),1):
        print('\t',j,j%3)


"""
matrix = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

for i in range(0,len(matrix),1):
    for j in range(0,len(matrix[i]),1):
        for x in range(0,len(matrix),1):
            for y in range(0,len(matrix[x]),1):
                print(f'[{i}][{j}]!=[{x}][{y}]')
"""

# What if we just hard code the constraints?