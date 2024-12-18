import networkx as nx
import numpy as np
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

def build_garden(rows, cols):
    G = nx.grid_2d_graph(rows, cols)  # Nodes are in (row, col) format

    # Add diagonal edges to the graph
    for i in range(rows):
        for j in range(cols):
            current_node = (i, j)
            # Add diagonal connections
            if i < rows - 1 and j < cols - 1:  # Bottom-right diagonal
                G.add_edge(current_node, (i + 1, j + 1))
            if i < rows - 1 and j > 0:  # Bottom-left diagonal
                G.add_edge(current_node, (i + 1, j - 1))

    for node in G.nodes():
        G.nodes[node]["state"]= 0
        G.nodes[node]["specie"]= {"apple": [2,4,6]}

    return (G)

rows, cols = 10, 10
G= build_garden(rows, cols)
print(G.nodes[(1, 1)])
color_map = []

G.nodes[(1,1)]["state"] =1
for node in G.nodes:
    if G.nodes[node]["state"] ==1:
        color_map.append("green")
        continue
    color_map.append("gray")

custom_labels = {}
for node in G.nodes:
        if G.nodes[node]["state"] ==0:
            custom_labels[node] = "empty"
        if G.nodes[node]["state"] ==1:
            custom_labels[node] = G.nodes[node]["specie"],"seed"
        if G.nodes[node]["state"] ==2:
            custom_labels[node] = "tree"
        if G.nodes[node]["state"] ==3:
            custom_labels[node] = "reock"

# Visualization of the graph
plt.figure(figsize=(10, 10))
pos = {(i, j): (j, -i) for i, j in G.nodes}  # Arrange nodes in grid format
nx.draw(G, pos,labels=custom_labels, with_labels=True, node_size=2000, node_color=color_map, font_size=10)
plt.show()


def print_neighbors(G, n):
  a= nx.all_neighbors(G,n)
  for x in a:
    print(x)  

def list_neighbors(G, n):
    list=[]
    a= nx.all_neighbors(G,n)
    for x in a:
        list.append(x)
    return list