from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # Use 'open' to open the file
    f = open(filename, "r")

    # Use the first line (G or D) to determine whether graph is directed 
    # and create a graph object
    first_line = f.readline().strip()
    graph = Graph(False)
    
    # If undirected
    if  first_line == "G":
        graph = Graph(False)
    
    # If directed
    elif first_line == "D":
        graph = Graph()
        
    else:
        print("Invalid Input")
        print(first_line)

    # Use the second line to add the vertices to the graph
    vertices = f.readline().strip()
    for _ in vertices:
        graph.add_vertex(_)

    # Use the 3rd+ line to add the edges to the graph
    for line in f:
        if line != '':
            print(line)
            curr = line.replace('(', '')
            curr = curr.replace(')', '').strip()
            curr = curr.split(",")
            print("Current line: {}".format(curr))
            
            if curr:
                vert1 = graph.add_vertex(curr[0])
                vert2 = graph.add_vertex(curr[1])
                # print("Vert 1: {} Vert 2: {}".format(vert1, vert2))
                
                graph.add_edge(vert1.get_id(), vert2.get_id())
        
    f.close()
    return graph