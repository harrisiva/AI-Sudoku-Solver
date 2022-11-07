from classes import Variable, Graph, CSP
import copy, math
from datetime import datetime

def revise(edge, board:list): 
    # Set up the variables
    xi:Variable = edge[0]
    xiOriginal,constraints,revised = copy.deepcopy(xi.value), edge[2], False

    # Make consistent (i.e., validate constraints and trim xi's domain)
    domain_copy = copy.deepcopy(xi.domain) # Removals will be done to this list (as the original will be iterated on)
    for x in xi.domain:
        board[xi.i][xi.j]=x # Temporarily set the cell to hold x (for constraint evaluation purposes)
        for constraint in constraints: 
            if eval(constraint)==False: # Since the constraints for this CSP are alldiff based, remove x if any of the constraints are not met
                if x in domain_copy: domain_copy.remove(x)

    # Update xi's domain if a removal function was called and update revised value based on the latter
    if len(domain_copy)!=len(xi.domain):
        xi.domain=copy.deepcopy(domain_copy)
        revised = True
    
    board[xi.i][xi.j] = copy.deepcopy(xiOriginal) # Reset the cell's value
    return revised

def ac3(csp:CSP, board:list): # NOTE: AC-3 is fine, there are no issues with it
    queue:list = [edge for edge in csp.graph.edges] # add all the arcs (edges) from the csp's graph to the "queue"
    with open('log.txt','a+') as file:
        file.write(f'{datetime.now()}:: Initial queue length:{len(queue)}\n')
        step_count = 0
        while len(queue)>0:
            arc = queue.pop() # order is irrelevant since it is commutative
            file.write(f'\t({step_count}):: Queue length:{len(queue)}\n')
            if revise(arc,board): # if there were any x in the from nodes domain that would never work with the to domain and was therefore trimmed
                if len(arc[0].domain)==0: return False # if no value in x, can be used as a consistent value with arc[0] with relation to arc[1], return false to indiciate that the problem is not solvable
                for edge in csp.graph.edges:  # Find all neighbots to arc[0] <- find edges that have edge[1]==arc[0] and add them back to the queue
                    if edge[1]==arc[0]: queue.append(edge)
            step_count+=1
    return True
