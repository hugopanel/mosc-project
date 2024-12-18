import networkx

def main():
    graph = networkx.Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'A')
    print('Nodes:', graph.nodes())
    print('Edges:', graph.edges())
    print('Neighbors of A:', graph.neighbors('A'))

if (__name__ == '__main__'):
    main()