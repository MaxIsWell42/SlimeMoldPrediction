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

    # Dijkstra's Algorithm - Shortest Path
    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        # Create a dictionary `vertex_to_distance` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_distance = {}
        for vertex in self.vertex_dict.values():
            vertex_to_distance[vertex] = float('inf')
            
        start_vertex = self.vertex_dict[start_id]
        vertex_to_distance[start_vertex] = 0

        # While `vertex_to_distance` is not empty:
        while vertex_to_distance:
        # 1. Get the minimum-distance remaining vertex, remove it from the
        #    dictionary. If it is the target vertex, return its distance.
            min_distance = min(vertex_to_distance.values())
            min_vertex = None
            
            for vertex in vertex_to_distance:
                if vertex_to_distance[vertex] == min_distance:
                    min_vertex = vertex
        
        # 2. Update that vertex's neighbors by adding the edge weight to the
        #    vertex's distance, if it is lower than previous.
            weight_of_neighbor = (
                list(min_vertex.neighbors_dict.values())
            )
            
            if min_vertex.id == target_id:
                return vertex_to_distance[min_vertex]
            
            for neighbor, weight in weight_of_neighbor:
                if neighbor in vertex_to_distance:
                    current_distance = vertex_to_distance[neighbor]
                    new_distance = weight + vertex_to_distance[min_vertex]
                    if new_distance < current_distance:
                        vertex_to_distance[neighbor] = new_distance

            del vertex_to_distance[min_vertex]

        # Return None if target vertex not found.
        return None

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