import math

class Variable:
    def __init__(self,name,domain):
        self.name = name #  String to represent the name of the node (in the map example)
        self.value = -1 # Default ==-1 which means its not holding any colors
        self.domain = domain # Domain of the values the list can hold (initiliazed with the CSP Declared variable)
        return
    
class Graph:
    def __init__(self):
        self.nodes: int = 0 # Number of nodes
        self.edges:list = [] # List of edges
        return
        
    def add_edge(self,node1,node2,constraint):
        # AC-3 CSP uses two way directed edges
        self.edges.append([node1,node2,constraint])
        self.nodes+=1
        return
    
    def view_graph(self): # Print as a list of edges
        print('From|To|Constraint')
        for edge in self.edges:
            print(f'{edge[0].name}|{edge[1].name}|{eval(edge[2])}')
        return

class CSP:
    def __init__(self, graph: Graph):
        self.variables=[] # Variable objects
        self.domain=[] # Domain for each variable or common, depending on the problem
        self.constaints=[] 
        self.graph = graph
        return


# Test the Graph DS and AC-3 with slide 17 example
CSP_domain = [0,1,2,3,4,5,6,7,8,9]
# Create the variables for the different states in AU
x = Variable('X',CSP_domain)
y = Variable('Y',CSP_domain)

# Create the graph by inserting edges
graph = Graph() # Initialize the graph object

# Add the edges
graph.add_edge(x,y,'x==math.sqrt(y)')
graph.add_edge(y,x,'y==(x*x)')

# Initializing CSP with the constraints
csp = CSP(graph)

# Add the variables
csp.variables.append(x)
csp.variables.append(y)

# Set the common domain of values
csp.domain=CSP_domain

# Set the constraints (in this case, just copy them from the edges to the csp data structure)
for edge in graph.edges: csp.constaints.append(edge[2])

def revise(edge): # edge[0]=Xi and edge[1]=Xj
    revised = False # Set revised initially to be false
    for x in edge[0].domain: # Iterate through the domain of x
        to_remove = True # Set to false when there is any combination with y with makes it consistent
        edge[0].value = x # set  x to be the value of the node (edge[0]) 
    
        for y in edge[1].domain: # loop through, if at any point the constraint between x and y is true, go to the next value of x
            edge[1].value = y # set y to be the value of the node (edge[1])
            if eval(edge[2]):
                to_remove = False
                break 
    
        if to_remove==True: # If this value of x, can never be consistent with the other variable, remove it
            edge[0].domain.remove(x)
            revised = True
    
    edge[0].value,edge[1].value = -1,-1 # reset both the edges to hold the default values (as this is not an assignment function)
    
    return revised

def ac3(csp:CSP):
    queue:list = [edge for edge in csp.graph.edges] # add all the arcs (edges) from the csp's graph to the "queue"
    print(queue)
    while len(queue)!=0:
        arc = queue.pop() #commutative, therefore, order is irrelevant
        print(f'\t{arc[0].name}:{arc[0].domain}')
        if revise(arc): # if there were any x in the from nodes domain that would never work with the to domain and was therefore trimmed
            if len(arc[0].domain)==0: return False # if no value in x, can be used as a consistent value with arc[0] with relation to arc[1], return false to indiciate that the problem is not solvable
            for edge in csp.graph.edges:  # Find all neighbots to arc[0] <- find edges that have edge[1]==arc[0] and add them back to the queue
                if edge[1]==arc[0]:queue.append(edge) 
    return True

if ac3(csp):
    print(csp.variables[0].domain)
    print(csp.variables[1].domain)