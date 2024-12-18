import networkx as nx
import numpy as np

def build_garden(rows, cols):
    # Create the graph
    G = nx.grid_2d_graph(rows, cols)

    # Map the nodes to numeric labels as per your description
    mapping = {(i, j): i * cols + j + 1 for i, j in G.nodes}
    G = nx.relabel_nodes(G, mapping)

    # Adding diagonal edges to the graph
    for i in range(rows):
        for j in range(cols):
            current_node = i * cols + j + 1
            # Add diagonal connections
            if i < rows - 1 and j < cols - 1:  # Bottom-right diagonal
                G.add_edge(current_node, (i + 1) * cols + (j + 1) + 1)
            if i < rows - 1 and j > 0:  # Bottom-left diagonal
                G.add_edge(current_node, (i + 1) * cols + (j - 1) + 1)

    pos = {node: (((node - 1) % cols), -((node - 1) // cols)) for node in G.nodes}

    return (G, pos)

rows, cols = 10, 10
G , pos= build_garden(rows, cols)


# Visualization of the graph
plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=10)
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