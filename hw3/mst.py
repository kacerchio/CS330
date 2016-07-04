'''

Kristel Tan (ktan@bu.edu), Johnson Lam (jlam17@bu.edu), & Andrew Lee (teayoon@bu.edu)
CAS CS330 Spring 2016 - Professor Byers
hw3 - mst.py

'''

import networkx as nx 
import random
import numpy as np
from networkx.utils import UnionFind
from itertools import combinations
   
# completeGraph() creates a complete undirected graph with weighted edges
# and returns the graph
   
def completeGraph(n):
    
    # Create complete undirected graph with n nodes and (n choose 2)
    # edges using networkx complete_graph library function
    g = nx.complete_graph(n)
    
    # Iterate through all edges and assign each one a random weight
    # uniformly distributed from [0, 1]
    for (u, v) in g.edges():
        rand_weight = random.uniform(0, 1)
        g.add_edge(u, v, weight=rand_weight)
    
    return g

# squareGraph() returns a complete graph where the vertices are 
# chosen uniformly inside the unit square and the edges have weights 
# which are the Euclidean distance between its vertices.

def squareGraph(n):
    
    # Generate list of uniformly random coordinates inside a square
    coordinates = []
    for i in range(n):
        coordinates.append((random.uniform(0, 1), random.uniform(0, 1)))
    
    # Add the list of vertices to a Graph() object
    g = nx.Graph()
    g.add_nodes_from(coordinates)
    
    # Creates edges between all vertices in the graph
    edges = combinations(coordinates, 2)
    g.add_edges_from(edges)
    
    # Calculates the edge weights
    for (c1,c2) in g.edges():
        u = np.array(c1)
        v = np.array(c2)
        g.add_edge(c1, c2, weight = np.linalg.norm(u-v))
        
    return g

# mst() returns the minimum spanning tree using networkx library 
# functions and implements Kruskal's algorithm

def mst(g, weight='weight', data=True):

    # Initialize a UnionFind() object to store the spanning edges of the MST
    mst = UnionFind()
    # Sort the edges in ascending order of their weights
    edges = sorted(g.edges(data = True), key = lambda t: t[2].get(weight, 1))
    
    # For each edge (u, v) by ordered weight, check if adding the edge
    # will create a cycle; if not, add to the mst, else discard the edge
    for (u, v, w) in edges:
        if mst[u] != mst[v]:
            yield (u, v, w) 
        mst.union(u, v)

# calcSum() iterates through a given minimum spanning tree and 
# calculates the sum of the weights in the tree

def calcSum(g, weight='weight', data=True):
    
    total_weight = 0
    for (u, v, w) in g.edges_iter(data=True):
        total_weight += w['weight']
    
    return total_weight
        
        
graph1 = completeGraph(6)
mst1 = nx.Graph(kruskal(graph1))

print(graph1.edges(data=True), '\n')
print(mst1.edges(data=True), '\n')
print(calcSum(mst1), '\n')

graph2 = squareGraph(6)
mst2 = nx.Graph(kruskal(graph2))

print(graph2.edges(data=True), '\n')
print(mst2.edges(data=True), '\n')
print(calcSum(mst2), '\n')
