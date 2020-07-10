from graphs.graph import Graph, Vertex

class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        self.neighbors_dict[vertex_obj.__id] = (vertex_obj, weight)
        return self.neighbors_dict

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        neighbor_ids = [
            neighbor for neighbor, weight 
            in list(self.neighbors_dict.values())
        ]
        return neighbor_ids

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        return list(self.neighbors_dict.values())
    
    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        """
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {} # id -> object
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        vertex = Vertex(vertex_id)
        self.vertex_dict[vertex_id] = vertex
        return vertex

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        vertex1 = self.get_vertex(vertex_id1)
        vertex2 = self.get_vertex(vertex_id2)
        
        # print("Vertex Id 1 {} Vertex Id 2 {}".format(vertex_id1, vertex_id2))
        vertex1.add_neighbor(vertex2, weight)
        
        if self.is_directed == False:
            vertex2.add_neighbor(vertex1, weight)
    
    # Kruskal's Algorithm - Find Edges of a Minimum-Spanning Tree
    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root


    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # Create a list of all edges in the graph, sort them by weight 
        # from smallest to largest
        edges = []

        # Got this from github.com/squeaky1273, clever way to simply sort the edges using sorted and an anonymous function
        for vertex in self.get_vertices():
            for neighbor, weight in vertex.get_neighbors_with_weights():
                edges.append((vertex.get_id(), neighbor.get_id(), weight))
        edges = sorted(edges, key=lambda item: item[2])

        # Create a dictionary `parent_map` to map vertex -> its "parent". 
        # Initialize it so that each vertex is its own parent.
        parent_map = {x[0]:x[0] for x in edges}

        # Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)
        solution = list()

        # While the spanning tree holds < V-1 edges, get the smallest 
        # edge. If the two vertices connected by the edge are in different sets 
        # (i.e. calling `find()` gets two different roots), then it will not 
        # create a cycle, so add it to the solution set and call `union()` on 
        # the two vertices.
        while len(solution) <= len(edges) - 1:
            current_edge = edges.pop(0)
            (v1, v2, weight) = current_edge
            if self.find(parent_map, v1) != self.find(parent_map, v2):
                solution.append(current_edge)
                self.union(parent_map, v1, v2)        

        # Return the solution list.
        return solution
    
    
    # Prim's Algorithm - Find the weight of a MST
    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.

        Assume that the graph is connected.
        """
        # Create a dictionary `vertex_to_weight` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_weight = {}
        for vertex in self.vertex_dict.values():
            vertex_to_weight[vertex] = float('inf')

        # Choose one vertex and set its weight to 0
        start = self.get_vertices()[0]
        vertex_to_weight[start] = 0 
        MST_weight = 0

        # While `vertex_to_weight` is not empty:
        while vertex_to_weight:
        # 1. Get the minimum-weighted remaining vertex, remove it from the
        #    dictionary, & add its weight to the total MST weight
        # 2. Update that vertex's neighbors, if edge weights are smaller than
        #    previous weights
            min_weight = min(vertex_to_weight.items(), key=lambda x: x[1])
            current_vertex = min_weight[0]
            vertex_to_weight.pop(current_vertex, None)
            MST_weight += min_weight[1]
            
            for vertex in current_vertex.get_neighbors_with_weights():
                neighbor, weight = vertex
                if neighbor in vertex_to_weight:
                    if weight < vertex_to_weight[neighbor]:
                        vertex_to_weight[neighbor] = weight

        # Return total weight of MST
        return MST_weight
        
    
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
        
        
    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """
        
        dist = {}
        vertex_ids = self.vertex_dict.keys()
        
        # Create a dictionary of all vertices and their possible connections
        for v1 in vertex_ids:
            dist[vertex1] = dict()
            for v2 in vertex_ids:
                dist[v1][v2] = WeightedGraph.INFINITY
            dist[v1][v1] = 0
        
        # Add all edge weights to the dict
        vertices = self.get_vertices()
        
        for vertex in vertices:
            weighted_neighbors = vertex.get_neighbors_with_weights()
            
            for neighbor, weight in weighted_neighbors:
                dist[vertex.get_id()][neighbor.get_id()] = weight
        
        for i in vertices:
            for j in vertices:
                for k in vertices:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                    
        return dist