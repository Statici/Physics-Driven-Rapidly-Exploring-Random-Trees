""" This is the "first" functional revision of the lichtenberg figure simulator.
    It generates a graph based on inverse-square-law contributions to a rapidly
    exploring random graph, but it's overly simplified (not physical at all).
"""
import numpy as np
from graphs import Graph
from numpy import sqrt as sqrt
from numpy import array as arr
from numpy.linalg import norm as norm
from random import uniform as rand
from collections import Counter
from graphviz import Graph as GraphvizGraph
import time

class LichtenbergGraph(Graph):
    """ Extension of the basic Graph class aimed to simulate Lichtenberg figures. """

    r = 1 # Global minimum spatial growth distance

    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = { 0 : { "neighbors" : [1],
                                 "loc" : arr([0,0]),
                                 "weight" : 1,
                                 "burnt" : 0
                                 },
                           1 : { "neighbors" : [0],
                                 "loc" : arr([r,r]),
                                 "weight" : 1,
                                 "burnt" : 0
                                }
                           }
        super().__init__(graph_dict)

    def locations(self):
        return [self._graph_dict[vertex]["loc"] for vertex in self._graph_dict]

    def get_nearest_vertex(self, new_loc):
        graph = self._graph_dict
        dists = {vertex : norm(graph[vertex]["loc"]-new_loc) for vertex in graph}
        return min(dists, key=dists.get)

    def is_too_close(self, new_loc):
        """ Determines if the position of a potential new vertex is within r of an existing vertex. """
        graph = self._graph_dict
        for vertex in graph:
            if norm(new_loc - graph[vertex]["loc"]) < self.r*1.4:
                return self.get_nearest_vertex(new_loc)
        return False

    def add_vertex(self, vertex, neigh=None, pos=None, w=1):
        """ Overloading of the Graph class's add_vertex, but with the new properties
            'loc' and 'burnt'.
        """
        super().add_vertex(vertex, neigh, w)
        self._graph_dict[vertex]["burnt"] = 0
        if pos is None: self._graph_dict[vertex]["loc"] = [0,0]
        else: self._graph_dict[vertex]["loc"] = pos

    def force(self, vertex1, vertex2):
        """ Calculates the inverse-r^2 force (given by the E field) between
            two charged points (vertices). Note the obvious difference with real
            physics: q1 + q2, not q1*q2. It just makes things that look nicer.
        """
        graph = self._graph_dict
        dx = graph[vertex2]["loc"][0] - graph[vertex1]["loc"][0]
        dy = graph[vertex2]["loc"][1] - graph[vertex1]["loc"][1]
        q1 = graph[vertex1]["weight"]
        q2 = graph[vertex2]["weight"]
        return (q1+q2)*arr([dx, dy])/(dx**2 + dy**2)**1.5

    def net_force(self, vertex1):
        """ Calculates net force on a single vertice given contributions from all other vertices. """
        graph = self._graph_dict
        F = arr([0.0,0.0])
        for vertex in graph:
            if vertex != vertex1:
                F += self.force(vertex, vertex1)
        return F

    def net_forces(self):
        """ Calculates net force on all vertices; used for calculating vertex expansion probabilities. """
        graph = self._graph_dict
        return {vertex : self.net_force(vertex) for vertex in graph}

    def pick_expansion_vertex(self):
        """ Based on the net force on each vertex, picks a vertex where higher net forces correspond
            to higher expansion probability.
            By default, if for whatever reason somehow P doesn't reach zero, returns first vertex.
        """
        graph = self._graph_dict
        forces = self.net_forces()
        total_force = sum([norm(forces[vertex]) for vertex in graph])
        P = rand(0,1)*total_force
        for vertex in forces:
            P -= norm(forces[vertex])
            if P <= 0:
                return vertex
        return 0

    def pick_expansion_point(self, vertex):
        """ Based on the net force direction on the target vertex, randomly picks a growth direction
            based on a uniform-distribution shift on the Fx and Fy components. A little silly,
            but a starting point. The step is of distance r from the growth vertex.
        """
        graph = self._graph_dict
        F = self.net_force(vertex)
        F[0] *= rand(0,1) + F[1]*rand(0,.3)
        F[1] *= rand(0,1) + F[0]*rand(0,.3)
        F *= self.r/norm(F)
        x0 = graph[vertex]["loc"]
        return x0+F

    def make_new_vertex(self):
        """ Spawns a new vertex, one that is not within r of any other vertex."
            If this new vertex is within r of another vertex, it will instead
            simply create a new edge from the growth vertex to that vertex.
            Big issue here: If it calls itself too many times, python will reach
            its maximum recursion depth of ~1,000.
        """
        expansion_vertex = self.pick_expansion_vertex()
        expansion_point = self.pick_expansion_point(expansion_vertex)
        if self.is_too_close(expansion_point) and expansion_vertex != self.is_too_close(expansion_point):
            self.make_new_vertex();
        else:
            self.add_vertex(str(len(self._graph_dict)), [expansion_vertex], expansion_point)
        self.set_active_states(expansion_vertex)

    def set_active_states(self, vertex):
        """ Uses the find_shortest_path function to find the shortest path to the root.
            Those vertices along the way then have their weights INCREASED, and
            all other vertices have their weights DECREASED.
            This should run after any vertex is grown, starting from it.
        """
        graph = self._graph_dict
        path = self.find_shortest_path(vertex, "0")
        notpath = np.setdiff1d(list(graph.keys()), path)
        for vertex in path:
            if graph[vertex]["burnt"] < 15:
                graph[vertex]["burnt"] += .005
            if vertex != "0":
                if graph[vertex]["weight"] < 1:
                    graph[vertex]["weight"] = 1
                elif graph[vertex]["weight"] < 2:
                    graph[vertex]["weight"] *= 1.1
        for vertex in notpath:
            if graph[vertex]["weight"] > .025:
                graph[vertex]["weight"] -= .025

    def return_current_graph(self):
        return self._graph_dict

if __name__ == "__main__":
    """ This will grow a graph of some number of vertices (n) starting from two
        close neighbors. It also uses graphviz to render some pictures that are
        well, honestly, *massive* (9616x9616). The visualizations it produces
        are not wonderful, but pretty neato nonetheless.
        Also note that this program runs in O(n^5) time (!) so be careful with
        how high you set n if you want the thing to actually complete.
    """
    g = {  "0" : { "neighbors" : ["1"],
                    "loc" : arr([0, 0]),
                    "weight" : 5,
                    "burnt" : 0
                    },
            "1" : { "neighbors" : ["0"],
                    "loc" : arr([1, 1]),
                    "weight" : 1,
                    "burnt" : 0
                    }
        }

    times = []
    full_time = time.time()
    iter_time = time.time()

    dot = GraphvizGraph('G',
                        filename = 'iteration_000',
                        engine = 'fdp',
                        format='png')

    graph = LichtenbergGraph(g)
    n = 50
    for i in range(n):
        """ Make a new vertex - the brunt work is done in this one line. """
        graph.make_new_vertex()
        """ Save the current state of the graph to .gv and .png files. """
        edges = graph.edges()
        fileName = "iteration_" + str(i) + ".gv"
        dot = GraphvizGraph('G',
                            filename=fileName,
                            engine='fdp',
                            format='png')
        for edge in edges:
            edge = list(edge)
            w = graph._graph_dict[edge[0]]["burnt"]
            w += graph._graph_dict[edge[1]]["burnt"]
            dot.edge(edge[0], edge[1], penwidth=str(w*10))
        for vertex in graph._graph_dict:
            x = graph._graph_dict[vertex]["loc"][0]
            y = graph._graph_dict[vertex]["loc"][1]
            w = graph._graph_dict[vertex]["burnt"]
            dot.node(vertex,
                     pos=str(x) + "," + str(y) + "!",
                     shape="point")
        """ If you do not use some base corner nodes, the png produced will grow
            in resolution slowly, which kinda looks...meh.
        """
        dot.node('corner1',
                 pos='-50,-50!',
                 shape="point")
        dot.node('corner2',
                 pos='50,50!',
                 shape="point")
        """ Saves the actual files. """
        dot.render()
        t2 = time.time()
        print("%i%% done, took %f seconds for last percent." % (int(i/n*100),t2-iter_time))
        iter_time = time.time()

    """ This last stuff just serves to produce a pdf image that pops up in your
        default pdf viewer program; omitting it still lets the images above be
        saved, but it's nice when running it the first few times for simplicity.
    """
    for edge in edges:
        edge = list(edge)
        if len(edge) == 2:
            w = graph._graph_dict[edge[0]]["burnt"]
            w += graph._graph_dict[edge[1]]["burnt"]
            dot.edge(edge[0], edge[1], penwidth=str(w*10))
    for vertex in graph._graph_dict:
        x = graph._graph_dict[vertex]["loc"][0]
        y = graph._graph_dict[vertex]["loc"][1]
        w = graph._graph_dict[vertex]["burnt"]
        dot.node(vertex,
                 pos=str(x) + "," + str(y) + "!",
                 shape="point")
    t = time.time()-full_time
    print("Took a total of " + str(t) + " seconds to finish.")
    dot.view()
