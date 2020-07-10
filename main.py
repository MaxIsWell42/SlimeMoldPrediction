from graphs.weighted_graph import WeightedGraph

""" The questions:
- How the slime mold will go from one vertex to another(Dijkstra's Algorithm), 
- How it will 'grow' out and around itself(find vertices n away), and 
- The possible final solution from one vertex to all the others without extra connections(Kruskal's Algorithm) 
"""

def mold_growth(self, start, table):
    """ For simulating slime mold growth, which finds the most efficient path between all nodes of nutrients
        
        Arguments: 
        start: The point to start at
        table: The simulated table with vertices representing food
    """
    
    
    pass

# Create a large, weighted, undirected graph for testing
def make_large_graph(self):
    graph = WeightedGraph(is_directed=False)
    vertex_a = graph.add_vertex('A')
    vertex_b = graph.add_vertex('B')
    vertex_c = graph.add_vertex('C')
    vertex_c = graph.add_vertex('D')
    vertex_c = graph.add_vertex('E')
    vertex_c = graph.add_vertex('F')
    vertex_c = graph.add_vertex('G')
    vertex_c = graph.add_vertex('H')
    vertex_c = graph.add_vertex('J')

    graph.add_edge('A','B', 4)
    graph.add_edge('A','C', 8)
    graph.add_edge('B','C', 11)
    graph.add_edge('B','D', 8)
    graph.add_edge('C','F', 1)
    graph.add_edge('C','E', 4)
    graph.add_edge('D','E', 2)
    graph.add_edge('D','G', 7)
    graph.add_edge('D','H', 4)
    graph.add_edge('E','F', 6)
    graph.add_edge('F','H', 2)
    graph.add_edge('G','H', 14)
    graph.add_edge('G','J', 9)
    graph.add_edge('H','J', 10)

    return graph

if __name__ == "__main__":
    
    pass