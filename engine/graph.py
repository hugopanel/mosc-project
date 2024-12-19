# GRAPH MODULE

import networkx as nx

import engine.entities
import engine.config


def generate_garden(rows, cols):
    g = nx.grid_2d_graph(rows, cols)  # Nodes are in (row, col) format

    # Add diagonal edges to the graph
    for i in range(rows):
        for j in range(cols):
            current_node = (i, j)
            # Add diagonal connections
            if i < rows - 1 and j < cols - 1:  # Bottom-right diagonal
                g.add_edge(current_node, (i + 1, j + 1))
            if i < rows - 1 and j > 0:  # Bottom-left diagonal
                g.add_edge(current_node, (i + 1, j - 1))

    for node in g.nodes():
        g.nodes[node]["type"] = engine.entities.TYPE_EMPTY
        g.nodes[node]["sicknesses"] = []
        g.nodes[node]["age"] = 0
        g.nodes[node]["code"] = []
        g.nodes[node]["growth"] = 0
        g.nodes[node]["health"] = engine.config.default_seed_starting_health
        g.nodes[node]["greatest_ancestor"] = None

    return g
