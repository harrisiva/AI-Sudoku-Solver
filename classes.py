class Variable:
    def __init__(self,name,i,j,value,domain):
        self.name = name #  String to represent the name of the node (in the map example)
        self.value = value 
        self.domain = domain # Domain of the values the list can hold (initiliazed with the CSP Declared variable)
        self.i,self.j = i,j
        return
    def __str__(self):
        return f'{self.name}|{self.value}|{self.domain}'

class Graph:
    def __init__(self):
        self.edges:list = [] # List of edges
        self.nodes: list = []
        return
        
    def add_edge(self,from_node:Variable,to_node:Variable,constraint:list):
        # AC-3 CSP uses two way directed edges
        self.edges.append([from_node,to_node,constraint])

        # update list of nodes (check if node exists, if not true, append to list of nodes)
        node_exists = False
        for node in self.nodes:
            if from_node.name==node.name:
                node_exists = True
        if node_exists==False: 
            self.nodes.append(from_node)
    
        return
    
    def view_graph(self): # Print as a list of edges
        print('From|To|Constraint')
        for edge in self.edges:
            print(f'{edge[0].name}|{edge[1].name}|{edge[2]}')
        return

class CSP:
    def __init__(self, graph: Graph):
        self.variables=[] # Variable objects
        self.domain=[] # Domain for each variable or common, depending on the problem
        self.constaints=[] 
        self.graph = graph
        return
    def __str__(self):
        returnable = ''
        for variable in self.variables:
            returnable += f'{variable.name}: {variable.domain}\n'
        return returnable
