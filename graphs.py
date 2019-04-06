

class Graph(object):
    """ Basic graph class. Contains typical graph-exploration
        functions, specifically those to find all paths between
        two vertices, the shortest path between two vertices,
        and the weighted-shortest path between two vertices.

        Based largely on https://www.python-course.eu/graphs_python.php
    """

    def __init__(self, graph_dict=None):
        """ Initializes a graph object.
            If no dictionary or None is given,
            an empty dictionary will be created.
        """
        if graph_dict == None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def vertices(self):
        """ Returns the vertices (their IDs) of the graph """
        return list(self._graph_dict.keys())

    def edges(self):
        """ Returns edges (pairs of vertices) of the graph """
        return self.__generate_edges()

    def add_vertex(self, vertex, neigh=None, w=1):
        """ If the vertex is not in self._graph_dict, a
            vertex will be created appropriately.
            Otherwise, if the vertex is there, does nothing.
        """
        if neigh == None:
            neigh = []
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = { "weight" : w,
                                         "neighbors" : neigh
                                         }

    def set_weight(self, vertex, weight):
        """ Each vertex has a weight; this is just simpler
            than storing weights on all edges. May be changed
            later if the final product isn't accurate.
        """
        self._graph_dict[vertex]["weight"] = weight

    def add_edge(self, edge):
        """ An edge is a pair of vertices (a set, tuple, or list).
            If the first of the two vertices is in _graph_dict,
            the second is added to its list of neighbors.
            If it is not in _graph_dict, it is added, and the second
            is added to its list of neighbors.
            Note that each pair can have multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self._graph_dict:
            if vertex2 not in self._graph_dict[vertex1]["neighbors"]:
                self._graph_dict[vertex1]["neighbors"].append(vertex2)
        else:
            self._graph_dict[vertex1] = {"neighbors" : [vertex2],
                                         "weight" : 1}

    def __generate_edges(self):
        """ Generates an array of sets, each set comprising either
            one or two vertices.
        """
        edges = []
        for vertex in self._graph_dict:
            for neighbor in self._graph_dict[vertex]["neighbors"]:
                if {neighbor, vertex} not in edges:
                    edges.append({vertex, neighbor})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
            res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ Finds all non-looping paths between the start and end vertices.
            If no path is found, an empty array is returned.
        """
        graph = self._graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]["neighbors"]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def get_path_weights(self, start_vertex, end_vertex):
        """ Returns the weights of paths between two points.
            Indices of each weight match indices of paths found with find_all_paths.
        """
        paths = self.find_all_paths(start_vertex, end_vertex)
        graph = self._graph_dict
        return [sum(graph[vertex]["weight"] for vertex in paths[i]) for i in range(len(paths))]

    def find_shortest_path(self, start_vertex, end_vertex):
        """ Given the set of weights from get_path_weights, finds and returns
            the path that is the easiest to traverse from start_vertex and end_vertex.
        """
        paths = self.find_all_paths(start_vertex, end_vertex)
        graph = self._graph_dict
        path_weights = self.get_path_weights(start_vertex, end_vertex)
        return paths[path_weights.index(max(path_weights))]

if __name__ == "__main__":
    """ Displays results of some of the above functions with the graph defined below """
    g = { "a" : { "neighbors" : ["d"],
                  "weight" : 1
                  },
          "b" : { "neighbors": ["c"],
                  "weight" : 1
                  },
          "c" : { "neighbors" : ["b", "c", "d", "e"],
                  "weight" : 1
                  },
          "d" : { "neighbors" : ["a", "c"],
                  "weight" : 1
                  },
          "e" : { "neighbors" : ["c", "b"],
                  "weight" : -5
                  },
          "f" : { "neighbors" : [],
                  "weight" : 1
                  }
    }

    graph = Graph(g)

    graph.add_vertex('g', ['e','d'])

    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print('All paths from vertex "a" to vertex "b":')
    path = graph.find_all_paths("a", "b")
    print(path)

    print('All paths from vertex "a" to vertex "f":')
    path = graph.find_all_paths("a", "f")
    print(path)

    print('All paths from vertex "c" to vertex "c":')
    path = graph.find_all_paths("c", "c")
    print(path)

    print('All paths from vertex "a" to vertex "b":')
    path = graph.find_all_paths("a", "b")
    print(path)

    print('Path weights from vertex "a" to vertex "b":')
    path_weights = graph.get_path_weights("a","b")
    print(path_weights)

    print('Shortest path between vertex "a" and vertex "b":')
    path = graph.find_shortest_path("a","b")
    print(path)
