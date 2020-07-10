from collections import deque
import random

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.__id] = vertex_obj
        return self.__neighbors_dict

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        self.__vertex_dict[vertex_id] = Vertex(vertex_id)
        return self.__vertex_dict[vertex_id]
        
    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        vertex1 = self.get_vertex(vertex_id1)
        vertex2 = self.get_vertex(vertex_id2)
        # print("Vertex Id 1 {} Vertex Id 2 {}".format(vertex_id1, vertex_id2))
        vertex1.add_neighbor(vertex2)
        
        if self.__is_directed == False:
            vertex2.add_neighbor(vertex1)
        
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.pop()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        queue = deque()
        visited = set()
        
        queue.append(self.get_vertex(start_id))
        
        for _ in range(target_distance):
            for _ in range(len(queue)):
                vertex = queue.pop()
                if vertex not in visited:
                    for neighbor in vertex.get_neighbors():
                        queue.appendleft(neighbor)
                    visited.add(vertex)
        
        found = []
        for vertex in queue:
            if vertex not in visited and vertex.get_id() not in found:
                found.append(vertex.get_id())
                
        return found

    def is_bipartite(self, start):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        # Get the starting vertex
        root = self.get_vertex(start)
        
        # Start the queue and first object
        queue = deque()
        queue.append(root)
        
        # Keep count of the visited vertices so we don't check them twice
        visited = set()
        
        # Instantiate a red set and blue set
        red = set()
        blue = set()
        
        i = 0
        
        # Set the root for red to build from
        red.add(root)
        
        while queue:
            color_set = []
            opp_set = []
            
            # Get the color from whatever we pop off the queue
            # Get the next vertex
            vertex = queue.popleft()
            if vertex in red:
                color_set, opp_set = red, blue
            else: 
                color_set, opp_set = blue, red
                
            
            visited.add(vertex)

            # Go through each neighbor from the vertex and add it into the corresponding set
            for neighbor in vertex.get_neighbors():
                # Only add the neighboring vertex if it has not been visited
                if neighbor not in visited:
                    queue.append(neighbor)
                    
                # If it's the same color, return False
                if neighbor in color_set:
                    return False
                
                # add the neighboring vertexes into the opposite color set
                opp_set.add(neighbor)
            i += 1
        # Otherwise, the graph is bipartite
        return True
    
    # Got some of this from @github.com/squeaky1273
    def get_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        visited = []
        queue = deque()
        final = []
        
        def connectionHelper(current):
            connections = []
            queue.append(current)
        
            # While there's still vertexes in the queue
            while queue:
                # Get the next vertex
                current = queue.pop()
                connections.append(current)
                
                # Get the neighbors for the current node
                print('Current: {}'.format(current))
                neighbors = self.get_vertex(current).get_neighbors()
                print(neighbors)
                
                # Go through all the neighbors and append them to the current vertex's list[Not working, returning list of vertices]
                for neighbor in neighbors:
                    if neighbor.get_id() not in visited:
                        queue.append(neighbor.get_id())
                        visited.append(neighbor.get_id())
                visited.append(current)
                
            return connections

        
        for vertex in self.get_vertices():
            vert_id = vertex.get_id()
            if vert_id not in visited:
                connects = connectionHelper(vert_id)
                visited.append(vert_id)
                final.append(connects)
        
        return final
            
    
    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        # Start by adding the start to the visited
        visited = {start_id: [start_id]}
        
        # Create a stack for DFS
        stack = set()
        stack.add(self.get_vertex(start_id))
        
        while stack:
            # Start off by getting a vertex
            vertex = stack.pop() 
            vert_id = vertex.get_id()
            
            # Get all the neighbors for the current vertex
            neighbors = vertex.get_neighbors()
            
            # Edge case
            if vert_id == target_id:
                break
            
            # Build the path
            for neighbor in neighbors:
                n_id = neighbor.get_id()
                
                if n_id not in visited:
                    stack.add(neighbor)
                    path = visited[vert_id]
                    path = path + [n_id]
                    visited[n_id] = path
        
        return visited[target_id]
    
    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set() # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        start_vertex = self.get_vertex(start_id)
        dfs_traversal_recursive(start_vertex)

    def cycle_helper(self, vertex, visited, stack):
        """Goes through the neighbors of a vertex and determines if it contains a cycle. 
        This is better as a helper function because it needs to be run once for each vertex and it's easier to do that recursively"""
        
        cycle = False
        visited.add(vertex)
        stack.append(vertex)
        neighbors = vertex.get_neighbors()
        
        for neighbor in neighbors:
            # If it's not already visited, check it's paths for a cycle
            if neighbor not in visited:
                cycle = self.cycle_helper(neighbor, visited, stack)
            
            # Otherwise, if it finds a neighbor already in a stack, it's a cycle
            elif neighbor in stack:
                return True
            
        stack.remove(vertex)
        
        if cycle == True:
            return True

    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        visited = set()
        values = self.__vertex_dict.values()
        stack = []
        
        # Go through the graph and check if nodes are visited
        for v in values:
            if v in visited:
                return False
        # If they aren't, check them for cycles
            else:
                if self.cycle_helper(v, visited, stack) == True:
                    return True
        
        return False
    
    def top_sort_helper(self, vertex, visited, stack):
        """Helper function to recursively check all neighbors of a vertex"""
        visited.add(vertex)
        neighbors = vertex.get_neighbors()
        
        for neighbor in neighbors:
            if neighbor not in visited:
                self.top_sort_helper(neighbor, visited, stack)
        
        stack.append(vertex)
        return stack
        
    
    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        # Create a stack to hold the vertex ordering.
        stack = []
        visited = set()
        vertices = self.__vertex_dict.values()
        
        # For each unvisited vertex, execute a DFS from that vertex.
        # On the way back up the recursion tree (that is, after visiting a 
        # vertex's neighbors), add the vertex to the stack.
        if self.contains_cycle() == False:
            for vertex in vertices:
                if vertex not in visited:
                    self.top_sort_helper(vertex, visited, stack) == True
                    
            # Reverse the contents of the stack and return it as a valid ordering.
            order = list()
            for _ in range(len(self.__vertex_dict)):
                order.append(stack.pop().get_id())
            return order