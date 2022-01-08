

from Graph_Types.adjacency_matrix import AdjacencyMatrix
from Graph_Types.adjacency_list import AdjacencyList
from Graph_Types.weighted_graph import WeightedGraph
from Graph_Types.unweighted_graph import UnweightedGraph
from Graph_Types.base_graph import BaseGraph
from Graph_Types.graph_exceptions import *


class Conversions:

    @staticmethod
    def weighted_to_unweighted_graph(weighted_graph):
        if not isinstance(weighted_graph, WeightedGraph):
            raise ConversionOperationError(f"{type(weighted_graph).__name__}: is not a WeightedGraph")

        new_graph = UnweightedGraph(True, weighted_graph.multiple_edges)

        for vertex in weighted_graph.vertices:
            new_graph.add_vertex(vertex.value)

        for vertex in weighted_graph.vertices:
            neighbors = vertex.get_neighbors()

            for neighbor in neighbors:
                if new_graph.multiple_edges:
                    for i in range(len(neighbor[1])):
                        new_graph.add_edge(vertex.value, neighbor[0])
                else:
                    new_graph.add_edge(vertex.value, neighbor[0])

        new_graph.set_directed(weighted_graph.directed)
        return new_graph

    @staticmethod
    def unweighted_to_weighted_graph(unweighted_graph, default_weight=0):
        if not isinstance(unweighted_graph, UnweightedGraph):
            raise ConversionOperationError(f"{type(unweighted_graph).__name__}: is not a UnweightedGraph")

        new_graph = WeightedGraph(True, unweighted_graph.multiple_edges, default_weight)

        for vertex in unweighted_graph.vertices:
            new_graph.add_vertex(vertex.value)

        for vertex in unweighted_graph.vertices:
            neighbors = vertex.get_neighbors()

            for neighbor in neighbors:
                if new_graph.multiple_edges:
                    for i in range(vertex.neighbors[neighbor]):
                        new_graph.add_edge(vertex.value, neighbor, default_weight)
                else:
                    new_graph.add_edge(vertex.value, neighbor, default_weight)

        new_graph.set_directed(unweighted_graph.directed)
        return new_graph

    @staticmethod
    def graph_to_adjacency_matrix(graph):
        if not isinstance(graph, BaseGraph):
            raise ConversionOperationError(f"{type(graph).__name__}: is not a Graph")

        new_matrix = AdjacencyMatrix(True)

        for vertex in graph.vertices:
            new_matrix.add_vertex(vertex.value)

        for vertex in graph.vertices:
            neighbors = vertex.get_neighbors()

            for neighbor in neighbors:
                if isinstance(neighbor, int) and not new_matrix.is_neighbor(vertex.value, neighbor):
                    new_matrix.add_edge(vertex.value, neighbor)
                elif isinstance(neighbor, list) and not new_matrix.is_neighbor(vertex.value, neighbor[0]):
                    new_matrix.add_edge(vertex.value, neighbor[0], min(neighbor[1]) if graph.multiple_edges else
                        neighbor[1])

        new_matrix.set_directed(graph.directed)
        return new_matrix

    @staticmethod
    def graph_to_adjacency_list(graph):
        if not isinstance(graph, BaseGraph):
            raise ConversionOperationError(f"{type(graph).__name__}: is not a Graph")

        new_list = AdjacencyList(True, graph.multiple_edges)

        for vertex in graph.vertices:
            new_list.add_vertex(vertex.value)

        for vertex in graph.vertices:
            neighbors = vertex.get_neighbors()

            for neighbor in neighbors:
                if isinstance(neighbor, int):
                    if new_list.multiple_edges:
                        for i in range(vertex.neighbors[neighbor]):
                            new_list.add_edge(vertex.value, neighbor)
                    else:
                        new_list.add_edge(vertex.value, neighbor)
                elif isinstance(neighbor, list):
                    if new_list.multiple_edges:
                        for i in range(len(neighbor[1])):
                            new_list.add_edge(vertex.value, neighbor[0], neighbor[1][i])
                    else:
                        new_list.add_edge(vertex.value, neighbor[0], neighbor[1])

        new_list.set_directed(graph.directed)
        return new_list

    @staticmethod
    def _adjacency_matrix_to_weighted_graph(adjacency_matrix):
        if not isinstance(adjacency_matrix, AdjacencyMatrix):
            raise ConversionOperationError(f"{type(adjacency_matrix).__name__}: is not an AdjacencyMatrix")

        new_graph = WeightedGraph(True, adjacency_matrix.multiple_edges)

        for vertex in adjacency_matrix.vertices:
            new_graph.add_vertex(vertex)

        for vertex in adjacency_matrix.vertices:
            neighbors = adjacency_matrix.get_vertex(vertex)

            for neighbor in neighbors[1]:
                weight = neighbor[1] if neighbor[1] is not None else 0
                new_graph.add_edge(vertex, neighbor[0], weight)

        new_graph.set_directed(adjacency_matrix.directed)
        return new_graph

    @staticmethod
    def _adjacency_matrix_to_unweighted_graph(adjacency_matrix):
        if not isinstance(adjacency_matrix, AdjacencyMatrix):
            raise ConversionOperationError(f"{type(adjacency_matrix).__name__}: is not an AdjacencyMatrix")

        new_graph = UnweightedGraph(True, adjacency_matrix.multiple_edges)

        for vertex in adjacency_matrix.vertices:
            new_graph.add_vertex(vertex)

        for vertex in adjacency_matrix.vertices:
            neighbors = adjacency_matrix.get_vertex(vertex)

            for neighbor in neighbors[1]:
                new_graph.add_edge(vertex, neighbor[0])

        new_graph.set_directed(adjacency_matrix.directed)
        return new_graph

    @staticmethod
    def adjacency_matrix_to_graph(adjacency_matrix, weighted=True):
        if weighted:
            return Conversions._adjacency_matrix_to_weighted_graph(adjacency_matrix)
        else:
            return Conversions._adjacency_matrix_to_unweighted_graph(adjacency_matrix)

    @staticmethod
    def _adjacency_list_to_weighted_graph(adjacency_list):
        new_graph = WeightedGraph(True, adjacency_list.multiple_edges)

        for vertex in adjacency_list.vertices:
            new_graph.add_vertex(vertex)

        for vertex in adjacency_list.vertices:
            neighbors = adjacency_list.get_vertex(vertex)

            for neighbor in neighbors[1]:
                weight = neighbor[1] if neighbor[1] is not None else 0
                new_graph.add_edge(vertex, neighbor[0], weight)

        new_graph.set_directed(adjacency_list.directed)
        return new_graph

    @staticmethod
    def _adjacency_list_to_unweighted_graph(adjacency_list):
        new_graph = UnweightedGraph(True, adjacency_list.multiple_edges)

        for vertex in adjacency_list.vertices:
            new_graph.add_vertex(vertex)

        for vertex in adjacency_list.vertices:
            neighbors = adjacency_list.get_vertex(vertex)

            for neighbor in neighbors[1]:
                new_graph.add_edge(vertex, neighbor[0])

        new_graph.set_directed(adjacency_list.directed)
        return new_graph

    @staticmethod
    def adjacency_list_to_graph(adjacency_list, weighted=True):
        if not isinstance(adjacency_list, AdjacencyList):
            raise ConversionOperationError(f"{type(adjacency_list).__name__}: is not an AdjacencyList")

        if weighted:
            return Conversions._adjacency_list_to_weighted_graph(adjacency_list)
        else:
            return Conversions._adjacency_list_to_unweighted_graph(adjacency_list)

    @staticmethod
    def adjacency_list_to_adjacency_matrix(adjacency_list):
        if not isinstance(adjacency_list, AdjacencyList):
            raise ConversionOperationError(f"{type(adjacency_list).__name__}: is not an AdjacencyList")

        new_matrix = AdjacencyMatrix(True)

        for vertex in adjacency_list.vertices:
            new_matrix.add_vertex(vertex)

        for vertex in adjacency_list.vertices:
            neighbors = adjacency_list.get_vertex(vertex)

            for neighbor in neighbors[1]:
                if isinstance(neighbor, int) and not new_matrix.is_neighbor(vertex, neighbor):
                    new_matrix.add_edge(vertex, neighbor)
                elif isinstance(neighbor, list):
                    if not new_matrix.is_neighbor(vertex, neighbor[0]):
                        new_matrix.add_edge(vertex, neighbor[0], neighbor[1])
                    elif new_matrix.adjacency_matrix[new_matrix.vertices[vertex], new_matrix.vertices[neighbor[0]]] > \
                            new_matrix.update_weight(neighbor[1]):
                        new_matrix.adjacency_matrix[new_matrix.vertices[vertex], new_matrix.vertices[neighbor[0]]] = \
                            new_matrix.update_weight(neighbor[1])

        new_matrix.set_directed(adjacency_list.directed)
        return new_matrix

    @staticmethod
    def adjacency_matrix_to_adjacency_list(adjacency_matrix):
        if not isinstance(adjacency_matrix, AdjacencyMatrix):
            raise ConversionOperationError(f"{type(adjacency_matrix).__name__}: is not an AdjacencyMatrix")

        new_list = AdjacencyList(True, adjacency_matrix.multiple_edges)

        for vertex in adjacency_matrix.vertices:
            new_list.add_vertex(vertex)

        for vertex in adjacency_matrix.vertices:
            neighbors = adjacency_matrix.get_vertex(vertex)

            for neighbor in neighbors[1]:
                weight = neighbor[1] if neighbor[1] is not None else None
                new_list.add_edge(vertex, neighbor[0], weight)

        new_list.set_directed(adjacency_matrix.directed)
        return new_list

    @staticmethod
    def directed_to_undirected(original):
        if not original.directed:
            raise ConversionOperationError(f"{type(original).__name__}: is not directed")

        if isinstance(original, UnweightedGraph):
            new_graph = UnweightedGraph(True, original.multiple_edges)

            for vertex in original.vertices:
                new_graph.add_vertex(vertex.value)

            for vertex in original.vertices:
                neighbors = vertex.get_neighbors()

                for neighbor in neighbors:
                    if new_graph.multiple_edges:
                        for i in range(vertex.neighbors[neighbor]):
                            new_graph.add_edge(vertex.value, neighbor)
                            new_graph.add_edge(neighbor, vertex.value)
                    else:
                        new_graph.add_edge(vertex.value, neighbor)
                        if not new_graph.get_vertex(neighbor).is_neighbor(vertex.value):
                            new_graph.add_edge(neighbor, vertex.value)

            new_graph.set_directed(False)
            return new_graph

        elif isinstance(original, WeightedGraph):
            new_graph = WeightedGraph(True, original.multiple_edges)

            for vertex in original.vertices:
                new_graph.add_vertex(vertex.value)

            for vertex in original.vertices:
                neighbors = vertex.get_neighbors()

                for neighbor in neighbors:
                    if new_graph.multiple_edges:
                        for i in range(len(neighbor[1])):
                            new_graph.add_edge(vertex.value, neighbor[0], neighbor[1][i])
                            new_graph.add_edge(neighbor[0], vertex.value, neighbor[1][i])
                    else:
                        new_graph.add_edge(vertex.value, neighbor[0], neighbor[1])
                        if not new_graph.get_vertex(neighbor[0]).is_neighbor(vertex.value):
                            new_graph.add_edge(neighbor[0], vertex.value, neighbor[1])

            new_graph.set_directed(False)
            return new_graph

        elif isinstance(original, AdjacencyList):
            new_list = AdjacencyList(True, original.multiple_edges)

            for vertex in original.vertices:
                new_list.add_vertex(vertex)

            for vertex in original.vertices:
                neighbors = original.get_vertex(vertex)

                for neighbor in neighbors[1]:
                    weight = neighbor[1] if neighbor[1] is not None else None
                    new_list.add_edge(vertex, neighbor[0], weight)
                    if original.multiple_edges:
                        new_list.add_edge(neighbor[0], vertex, weight)
                    elif vertex not in [neighbor[0] for neighbor in original.get_vertex(neighbor[0])[1]]:
                        new_list.add_edge(neighbor[0], vertex, weight)

            new_list.set_directed(False)
            return new_list

        elif isinstance(original, AdjacencyMatrix):
            new_matrix = AdjacencyMatrix(True, original.multiple_edges)

            for vertex in original.vertices:
                new_matrix.add_vertex(vertex)

            for vertex in original.vertices:
                neighbors = original.get_vertex(vertex)

                for neighbor in neighbors[1]:
                    weight = neighbor[1] if neighbor[1] is not None else None
                    new_matrix.add_edge(vertex, neighbor[0], weight)
                    if vertex not in [neighbor[0] for neighbor in original.get_vertex(neighbor[0])[1]]:
                        new_matrix.add_edge(neighbor[0], vertex, weight)

            new_matrix.set_directed(False)
            return new_matrix
