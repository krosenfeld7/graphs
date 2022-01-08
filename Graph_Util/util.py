

from Graph_Types.adjacency_matrix import AdjacencyMatrix
from Graph_Types.adjacency_list import AdjacencyList
from Graph_Types.weighted_graph import WeightedGraph
from Graph_Types.unweighted_graph import UnweightedGraph


class Util:

    @staticmethod
    def create_adjacency_list(directed, vertices, edges):
        adjacency_list = AdjacencyList(True, True)
        multiple_edges = False

        for vertex in vertices:
            adjacency_list.add_vertex(vertex)

        for edge in edges:
            weight = None if len(edge) < 3 else edge[2]
            vertex1 = edge[0]
            vertex2 = edge[1]

            neighbors_vertex1 = [neighbor[0] for neighbor in adjacency_list.get_vertex(vertex1)[1]]
            neighbors_vertex2 = [neighbor[0] for neighbor in adjacency_list.get_vertex(vertex2)[1]]

            if vertex2 in neighbors_vertex1 or (not directed and vertex1 in neighbors_vertex2):
                multiple_edges = True

            adjacency_list.add_edge(vertex1, vertex2, weight)

            if not directed:
                adjacency_list.add_edge(vertex2, vertex1, weight)

        adjacency_list.multiple_edges = multiple_edges
        return adjacency_list


    @staticmethod
    def create_adjacency_matrix(directed, vertices, edges):
        adjacency_matrix = AdjacencyMatrix(True)

        for vertex in vertices:
            adjacency_matrix.add_vertex(vertex)

        for edge in edges:
            weight = None if len(edge) < 3 else edge[2]
            vertex1 = edge[0]
            vertex2 = edge[1]

            neighbors_vertex1 = [neighbor[0] for neighbor in adjacency_matrix.get_vertex(vertex1)[1]]
            neighbors_vertex2 = [neighbor[0] for neighbor in adjacency_matrix.get_vertex(vertex2)[1]]

            if vertex2 not in neighbors_vertex1:
                adjacency_matrix.add_edge(vertex1, vertex2, weight)

            if not directed and vertex1 not in neighbors_vertex2:
                adjacency_matrix.add_edge(vertex2, vertex1, weight)

        return adjacency_matrix

    @staticmethod
    def create_weighted_graph(directed, vertices, edges):
        weighted_graph = WeightedGraph(True, True)
        multiple_edges = False

        for vertex in vertices:
            weighted_graph.add_vertex(vertex)

        for edge in edges:
            weight = None if len(edge) < 3 else edge[2]
            vertex1 = edge[0]
            vertex2 = edge[1]

            if weighted_graph.get_vertex(vertex1).is_neighbor(vertex2) or \
                    (not directed and weighted_graph.get_vertex(vertex2).is_neighbor(vertex1)):
                multiple_edges = True

            weighted_graph.add_edge(vertex1, vertex2, weight)

            if not directed:
                weighted_graph.add_edge(vertex2, vertex1, weight)

        weighted_graph.multiple_edges = multiple_edges
        return weighted_graph

    @staticmethod
    def create_unweighted_graph(directed, vertices, edges):
        unweighted_graph = UnweightedGraph(True, True)
        multiple_edges = False

        for vertex in vertices:
            unweighted_graph.add_vertex(vertex)

        for edge in edges:
            vertex1 = edge[0]
            vertex2 = edge[1]

            if unweighted_graph.get_vertex(vertex1).is_neighbor(vertex2) or \
                    (not directed and unweighted_graph.get_vertex(vertex2).is_neighbor(vertex1)):
                multiple_edges = True

            unweighted_graph.add_edge(vertex1, vertex2)

            if not directed:
                unweighted_graph.add_edge(vertex2, vertex1)

        unweighted_graph.multiple_edges = multiple_edges
        return unweighted_graph
