# GRAPH MODULE

import networkx as nx


def generate_garden(rows, cols):
    # Create the graph
    g = nx.grid_2d_graph(rows, cols)

    # Map the nodes to numeric labels as per your description
    mapping = {(i, j): i * cols + j + 1 for i, j in g.nodes}
    g = nx.relabel_nodes(g, mapping)

    # Adding diagonal edges to the graph
    for i in range(rows):
        for j in range(cols):
            current_node = i * cols + j + 1
            # Add diagonal connections
            if i < rows - 1 and j < cols - 1:  # Bottom-right diagonal
                g.add_edge(current_node, (i + 1) * cols + (j + 1) + 1)
            if i < rows - 1 and j > 0:  # Bottom-left diagonal
                g.add_edge(current_node, (i + 1) * cols + (j - 1) + 1)

    pos = {node: (((node - 1) % cols), -((node - 1) // cols)) for node in g.nodes}

    return g, pos
