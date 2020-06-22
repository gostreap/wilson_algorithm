import networkx as nx
import matplotlib.pyplot as plt
from random import sample
import math


def complete_graph(n):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(n):
            G.add_edge(i, j)
    return G


def complete_pos(n):
    pos = dict()
    module = n
    for i in range(n):
        arg1 = module * math.cos(2 * math.pi * i / n)
        arg2 = module * math.sin(2 * math.pi * i / n)
        pos[i] = (arg1, arg2)
    return pos


def grid_graph(n):
    G = nx.Graph()
    G.add_nodes_from(range(n*n))
    for i in range(n):
        for j in range(n):
            if i > 0:
                G.add_edge(i*n+j, (i-1)*n+(j))
            if j > 0:
                G.add_edge(i*n+j, (i)*n+(j-1))
            if i < n-1:
                G.add_edge(i*n+j, (i+1)*n+(j))
            if j < n-1:
                G.add_edge(i*n+j, (i)*n+(j+1))
    return G


def grid_pos(n):
    pos = dict()
    for i in range(n):
        for j in range(n):
            pos[i*n+j] = (i, j)
    return pos


def triangle_coordinate_to_node(i, j):
    return int(i*(i+1)/2+j)


def triangle_graph(n):
    G = nx.Graph()
    vertices = G.add_nodes_from(range(int(n*(n+1)/2)))
    for i in range(n):
        for j in range(i+1):
            if j > 0:
                G.add_edge(triangle_coordinate_to_node(i, j),
                           triangle_coordinate_to_node(i, j-1))
            if j < i:
                G.add_edge(triangle_coordinate_to_node(i, j),
                           triangle_coordinate_to_node(i, j+1))
            if i < n-1:
                G.add_edge(triangle_coordinate_to_node(i, j),
                           triangle_coordinate_to_node(i+1, j))
            if j < i+1 and i < n-1:
                G.add_edge(triangle_coordinate_to_node(i, j),
                           triangle_coordinate_to_node(i+1, j+1))
    return G


def triangle_pos(n):
    pos = dict()
    for i in range(n):
        for j in range(i+1):
            pos[triangle_coordinate_to_node(i, j)] = (-i, j)
    return pos


def random_neighbour_from(G, node):
    return sample(list(G.neighbors(node)), 1)[0]


def add_path(T, path):
    for i in range(len(path) - 1):
        T.add_edge(path[i], path[i+1])


def random_walk(G, T):
    diff = set(G.nodes()) - set(T.nodes())
    path = []
    vertex = sample(diff, 1)[0]
    path.append(vertex)
    while vertex in diff:
        vertex = random_neighbour_from(G, vertex)
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
    T = nx.Graph()
    start = sample(G.nodes(), 1)[0]
    T.add_node(start)
    while T.number_of_nodes() != G.number_of_nodes():
        path = random_walk(G, T)
        path = remove_cycles(path)
        add_path(T, path)
    return T


if __name__ == "__main__":
    N = 20
    G = nx.barabasi_albert_graph(20, 5)
    #G = grid_graph(N)
    #pos = complete_pos(N)
    # print(pos)
    # G = grid_graph(N)
    # pos = grid_pos(N)
    T = wilson(G)
    pos1 = nx.spring_layout(G)
    nx.draw(G, pos=pos1, node_size=20)
    nx.draw(T, pos=pos1, node_size=20,
            edge_color="#FF0000", width=3.0)
    plt.show()
