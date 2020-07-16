from graphs.weighted_graph import WeightedGraph
from graphs.graph import Graph

""" The questions:
- How the slime mold will go from one vertex to another(Dijkstra's Algorithm), 
- How it will 'grow' out and around itself(find vertices n away), and 
- The possible final solution from one vertex to all the others without extra connections(Prim's Algorithm) 
"""

# Find all nodes n away as the slime mold expands in growth
def mold_growth(self, start, search_range):
    """ For finding all of the nodes around within a certain range, simulating mold exploring around itself for food
    """
    food = list()
    
    # Find all nodes of food around the starting point, simulating the mold growing out in all directions
    for dist in range(search_range):
        current_found = Graph.find_vertices_n_away(start, dist)
        if current_found not in food:
            food.append(current_found)
    return food


# Create a large, weighted, undirected graph of food nodes
def make_food_table():
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
    graph = make_food_table()
    # In these cases, I'm using A as the point where the mold is introduced into the environment
    # Finding the shortest path from the start point to food, could be between anywhere
    shortest_path = graph.WeightedGraph.find_shortest_path('A', 'J')
    
    # Finding all nodes of food around the start of mold growth, in this case within a distance of 6
    food_in_vicinity = graph.mold_growth('a', 6)
    
    # Finding what the slime mold would look like if it didn't have the extra connections between nodes
    mold_no_extra = graph.minimum_spanning_tree_prim()