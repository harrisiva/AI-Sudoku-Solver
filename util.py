from constants import *
import numpy as np

def viewBoard(variables, assignments):
    for variable in variables:
        print(f'Variable: {variable} Index: {(ROW_LETTER_AS_KEY[variable[0]],int(variable[1])-1)}')
    return