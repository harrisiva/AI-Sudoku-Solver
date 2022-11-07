def constraints_helper(x, y, w, z):
    with open("constraints2.txt","a") as f:
        for i in range(x, y):
            for j in range(w, z):
                for k in range(x,y):
                    for l in range(w, z):
                        if (k,l) != (i, j):
                            temp = f'board[{i}][{j}]!=board[{k}][{l}]'
                            f.write(f'{temp}\n')
def constraints():
    constraints_helper(0,3, 0,3)
    constraints_helper(0,3, 3,6)
    constraints_helper(0,3, 6,9)
    constraints_helper(3,6, 0,3)
    constraints_helper(3,6, 3,6)
    constraints_helper(3,6, 6,9)
    constraints_helper(6,9, 0,3)
    constraints_helper(6,9, 3,6)
    constraints_helper(6,9, 6,9)
    return
