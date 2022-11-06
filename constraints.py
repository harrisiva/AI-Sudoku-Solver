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
def constraints(x, y, w, z):
    f = open("constraints2.txt", "a")

    for i in range(x, y):
        for j in range(w, z):
            for k in range(x,y):
                for l in range(w, z):
                    if (k,l) != (i, j):
                        temp = f'board[{i}][{j}]!=board[{k}][{l}]'
                        f.write(f'{temp}\n')
                        print("board[",i,"]","[",j,"]!=","board[",k,"]","[",l,"]" ) # have to fix spacing here
    f.close()
constraints(0,3, 0,3)
constraints(0,3, 3,6)
constraints(0,3, 6,9)

constraints(3,6, 0,3)
constraints(3,6, 3,6)
constraints(3,6, 6,9)

constraints(6,9, 0,3)
constraints(6,9, 3,6)
constraints(6,9, 6,9)
