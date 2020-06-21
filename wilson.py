import networkx as nx
import matplotlib.pyplot as plt
from random import sample
import math


class Graph:
    def __init__(self, vertices=[], edges=[]):
        """create a new graph

        :param vertices: list of vertex labels
        :param edges: list of tuples (vertex_1, vertex_2) - vertex_* must belong to vertices
        """
        self.vertices = set(vertices)
        self.edges = dict()

        for vertex in self.vertices:
            self.edges[vertex] = set()

        for (vertex_1, vertex_2) in edges:
            self.edges[vertex_1].add(vertex_2)
            self.edges[vertex_2].add(vertex_1)

    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        self.edges[vertex] = set()

    def add_edge(self, vertex_1, vertex_2):
        if vertex_1 not in self.vertices:
            self.add_vertex(vertex_1)
        if vertex_2 not in self.vertices:
            self.add_vertex(vertex_2)
        self.edges[vertex_1].add(vertex_2)
        self.edges[vertex_2].add(vertex_1)

    def add_path(self, path):
        for i in range(len(path)-1):
            self.add_edge(path[i], path[i+1])

    def random_neighbour_from(self, vertex):
        return sample(self.edges[vertex], 1)[0]

    def to_nx_graph(self):
        n = self.vertices.copy()
        e = set()
        for node_1 in self.vertices:
            for node_2 in self.edges[node_1]:
                if (node_1, node_2) not in e and (node_2, node_1) not in e:
                    e.add((node_1, node_2))
        G = nx.Graph()
        G.add_nodes_from(n)
        G.add_edges_from(e)
        return G

    def show(self):
        nx.draw(self.to_nx_graph())
        plt.show()

    def __str__(self):
        s = "vertices : " + str(self.vertices)
        for vertex in self.vertices:
            s += "\nneighbours of " + \
                str(vertex) + " : " + str(self.edges[vertex])
        return s


def complete_graph(n):
    vertices = list(range(n))
    edges = []
    for i in range(n):
        for j in range(n):
            edges.append((i, j))
    return Graph(vertices=vertices, edges=edges)


def complete_pos(n):
    pos = dict()
    module = n
    for i in range(n):
        arg1 = module * math.cos(2 * math.pi * i / n)
        arg2 = module * math.sin(2 * math.pi * i / n)
        pos[i] = (arg1, arg2)
    return pos


def grid_graph(n):
    vertices = list(range(n*n))
    edges = []
    for i in range(n):
        for j in range(n):
            if i > 0:
                edges.append((i*n+j, (i-1)*n+(j)))
            if j > 0:
                edges.append((i*n+j, (i)*n+(j-1)))
            if i < n-1:
                edges.append((i*n+j, (i+1)*n+(j)))
            if j < n-1:
                edges.append((i*n+j, (i)*n+(j+1)))
    return Graph(vertices=vertices, edges=edges)


def grid_pos(n):
    pos = dict()
    for i in range(n):
        for j in range(n):
            pos[i*n+j] = (i, j)
    return pos


def triangle_coordinate_to_node(i, j):
    return int(i*(i+1)/2+j)


def triangle_graph(n):
    vertices = list(range(int(n*(n+1)/2)))
    edges = []
    for i in range(n):
        for j in range(i+1):
            if j > 0:
                edges.append((triangle_coordinate_to_node(i, j),
                              triangle_coordinate_to_node(i, j-1)))
            if j < i:
                edges.append((triangle_coordinate_to_node(i, j),
                              triangle_coordinate_to_node(i, j+1)))
            if i < n-1:
                edges.append((triangle_coordinate_to_node(i, j),
                              triangle_coordinate_to_node(i+1, j)))
            if j < i+1 and i < n-1:
                edges.append((triangle_coordinate_to_node(i, j),
                              triangle_coordinate_to_node(i+1, j+1)))
    return Graph(vertices=vertices, edges=edges)


def triangle_pos(n):
    pos = dict()
    for i in range(n):
        for j in range(i+1):
            pos[triangle_coordinate_to_node(i, j)] = (-i, j)
    return pos


def random_walk(G, T):
    diff = G.vertices - T.vertices
    path = []
    vertex = sample(diff, 1)[0]
    path.append(vertex)
    while vertex in diff:
        vertex = G.random_neighbour_from(vertex)
        path.append(vertex)
    return path


def remove_cycles(path):
    no_cycle = False
    while not no_cycle:
        no_cycle = True
        for i in range(len(path)):
            for j in range(i+1, len(path)):
                if path[i] == path[j]:
                    no_cycle = False
                    path = [path[k]
                            for k in range(len(path)) if not (k >= i and k < j)]
                    break
            if not no_cycle:
                break
    return path


def wilson(G):
    T = Graph()
    start = sample(G.vertices, 1)[0]
    T.add_vertex(start)
    while len(T.vertices) != len(G.vertices):
        path = random_walk(G, T)
        path = remove_cycles(path)
        T.add_path(path)
    return T


if __name__ == "__main__":
    N = 50
    G = complete_graph(N)
    pos = complete_pos(N)
    print(pos)
    # G = grid_graph(N)
    # pos = grid_pos(N)
    T = wilson(G)
    nx.draw(G.to_nx_graph(), pos=pos, node_size=20)
    nx.draw(T.to_nx_graph(), pos=pos, node_size=20,
            edge_color="#FF0000", width=3.0)
    plt.show()
