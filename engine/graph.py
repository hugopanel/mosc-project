# GRAPH MODULE

import networkx


def generate_graph(size_x, size_y):
    graph = networkx.Graph()
    for x in range(size_x):
        for y in range(size_y):
            if x > 0:
                graph.add_edge((x, y), (x - 1, y))
            if y > 0:
                graph.add_edge((x, y), (x, y - 1))
