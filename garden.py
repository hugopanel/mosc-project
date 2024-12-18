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
    return (G)

rows, cols = 10, 10
G = build_garden(rows, cols)

tree_dict = {"tree1": {"ADN": [0,3,6], "nodes":[]},
             "tree2": {"ADN": [0,3,6], "nodes":[]}}

print(tree_dict)
color_map = []
for node in G.nodes:
    if node in tree_dict["tree1"]["nodes"]:
        color_map.append("green")
        continue

custom_labels = {}
for node in G.nodes:
    for tree_name, tree_data in tree_dict.items():
        if node in tree_data["nodes"]:
            custom_labels[node] = tree_name

# Visualization of the graph
plt.figure(figsize=(10, 10))
pos = {(i, j): (j, -i) for i, j in G.nodes}  # Arrange nodes in grid format
nx.draw(G, pos,labels=custom_labels, with_labels=True, node_size=1000, node_color=color_map, font_size=10)
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