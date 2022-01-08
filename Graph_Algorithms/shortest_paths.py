

from Graph_Algorithms.algorithm_exceptions import *
from Graph_Util.conversions import Conversions
from math import inf
from sys import maxsize
from copy import deepcopy


class ShortestPaths:

    def __init__(self, graph=None):
        self._graph = graph
        self._type = type(self._graph).__name__
        if self._type not in ["UnweightedGraph", "WeightedGraph", "AdjacencyList", "AdjacencyMatrix"]:
            raise UnsupportedGraphTypeError(f"Invalid graph type: {self._type}")

    def _graph_min_distance(self, spt_set, distances):
        next_vertex = None
        min_dist = maxsize

        for vertex in spt_set:
            vertex_node = self._graph.get_vertex(vertex)
            if vertex_node.disconnected():
                continue

            neighbors = vertex_node.get_neighbors()
            curr_dist = distances[spt_set.index(vertex)]

            for neighbor in neighbors:
                if isinstance(neighbor, int) and neighbor not in spt_set:
                    if next_vertex is None or (next_vertex and next_vertex > neighbor):
                        next_vertex = neighbor
                        min_dist = curr_dist + 1
                elif isinstance(neighbor, list) and neighbor[1] + curr_dist < min_dist and neighbor[0] not in spt_set:
                    next_vertex = neighbor[0]
                    min_dist = neighbor[1] + curr_dist

        if next_vertex is not None:
            spt_set.append(next_vertex)
            distances.append(min_dist)

    def _adjacency_min_distance(self, spt_set, distances):
        next_vertex = None
        min_dist = maxsize

        for vertex in spt_set:
            vertex_node = self._graph.get_vertex(vertex)
            if len(vertex_node[1]) == 0:
                continue

            neighbors = vertex_node[1]
            neighbors = [node if node[1] is not None else [node[0], 1] for node in neighbors]
            curr_dist = distances[spt_set.index(vertex)]

            for neighbor in neighbors:
                if neighbor[1] + curr_dist < min_dist and neighbor[0] not in spt_set:
                    next_vertex = neighbor[0]
                    min_dist = neighbor[1] + curr_dist

        if next_vertex is not None:
            spt_set.append(next_vertex)
            distances.append(min_dist)

    def dijkstras(self, start_node=None):
        spt_set = []
        distances = []

        if 'Graph' in self._type:
            start_node = self._graph.get_vertex(start_node) if start_node else self._graph.get_start_vertex()
            spt_set.append(start_node.value)
            distances.append(0)

            for i in range(len(self._graph.vertices)):
                self._graph_min_distance(spt_set, distances)

            return [start_node.value, dict([(spt_set[i], distances[i]) for i in range(len(spt_set))])]
        else:
            if start_node is None:
                start_node = self._graph.get_start_vertex()

            spt_set.append(start_node)
            distances.append(0)

            for i in range(len(self._graph.vertices)):
                self._adjacency_min_distance(spt_set, distances)

            return [start_node, dict([(spt_set[i], distances[i]) for i in range(len(spt_set))])]

    def floyd_warshall(self):
        adjacency_matrix = self._graph

        if 'Graph' in self._type:
            adjacency_matrix = Conversions.graph_to_adjacency_matrix(adjacency_matrix)
        elif self._type == 'AdjacencyList':
            adjacency_matrix = Conversions.adjacency_list_to_adjacency_matrix(adjacency_matrix)

        dist_dict = {}
        distances = []

        for row in adjacency_matrix.vertices:
            for col in adjacency_matrix.vertices:
                matrix_dist = adjacency_matrix.adjacency_matrix[adjacency_matrix.vertices[row],
                                                                adjacency_matrix.vertices[col]]
                matrix_dist = inf if matrix_dist == 0 else matrix_dist
                if matrix_dist == 2:
                    matrix_dist -= 1
                elif matrix_dist > 1:
                    matrix_dist -= 2

                dist_dict[(row, col)] = matrix_dist

        dist_dict = dict(sorted(dist_dict.items()))

        for vertex in sorted(adjacency_matrix.vertices):
            vertex_row = list()
            for pair in dist_dict:
                if pair[0] == vertex:
                    if pair[0] == pair[1] and dist_dict[pair] == inf:
                        vertex_row.append(0)
                    else:
                        vertex_row.append(dist_dict[pair])

            distances.append(vertex_row)

        for k in range(len(adjacency_matrix.vertices)):
            for i in range(len(adjacency_matrix.vertices)):
                for j in range(len(adjacency_matrix.vertices)):
                    if distances[i][k] == inf or distances[k][j] == inf:
                        continue

                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

        output = {}
        for row in sorted(adjacency_matrix.vertices):
            vertex_paths = []
            for col in sorted(adjacency_matrix.vertices):
                vertex_paths.append([col, distances[row][col]])

            output[row] = vertex_paths
            row += 1

        return output

    def _get_edges(self):
        edges = {}

        for vertex in self._graph.vertices:
            if 'Graph' in self._type:
                neighbors = vertex.get_neighbors()

                for edge in neighbors:
                    if isinstance(edge, int):
                        if (vertex.value, edge) not in edges and (edge, vertex.value) not in edges:
                            edges[(vertex.value, edge)] = 1
                    elif (vertex.value, edge[0]) not in edges and (edge[0], vertex.value) not in edges:
                        edges[(vertex.value, edge[0])] = edge[1]
            else:
                neighbors = self._graph.get_vertex(vertex)[1]

                for edge in neighbors:
                    if isinstance(edge, int):
                        if (vertex, edge) not in edges and (edge, vertex) not in edges:
                            edges[(vertex, edge)] = 1
                    elif (vertex, edge[0]) not in edges and (edge[0], vertex) not in edges:
                        edges[(vertex, edge[0])] = edge[1]

        edges = sorted(edges.items(), key=lambda x: x[0])
        edges = [[*edge[0], edge[1]] for edge in edges]
        return edges

    def bellman_ford(self, start_node=None):
        if start_node is None:
            start_node = self._graph.get_start_vertex()

        distances = dict()
        edges = self._get_edges()

        if 'Graph' in self._type:
            for vertex in sorted(self._graph.vertices, key=lambda x: x.value):
                distances[vertex.value] = inf if vertex.value != start_node else 0
        else:
            for vertex in sorted(self._graph.vertices):
                distances[vertex] = inf if vertex != start_node else 0

        for i in range(len(self._graph.vertices) - 1):
            for vertex1, vertex2, weight in edges:
                weight = 0 if weight is None else weight
                if distances[vertex1] != inf and distances[vertex1] + weight < distances[vertex2]:
                    distances[vertex2] = distances[vertex1] + weight

        return distances

    def johnsons(self):
        raise AlgorithmNotImplementedError("Johnsons is unsupported")

        new_graph = deepcopy(self._graph)
        original_graph = deepcopy(self._graph)

        for vertex in self._graph.vertices:
            new_graph.remove_vertex(vertex.value if 'Graph' in self._type else vertex)

        new_graph.add_vertex(inf)
        if self._type == 'WeightedGraph':
            new_graph.default_weight = 0

        self._graph = new_graph + self._graph

        reweight = self.bellman_ford(inf)
        self._graph.remove_vertex(inf)
        del reweight[inf]

        edges = self._get_edges()

        print(self._graph)

        for vertex1, vertex2, weight in edges:
            if weight is None:
                weight = 0

            self._graph.remove_edge(vertex1, vertex2)
            self._graph.add_edge(vertex1, vertex2, (weight + reweight[vertex1] - reweight[vertex2]))

        print(self._graph)
        print(reweight)

        distances = dict()

        for vertex in self._graph.vertices:
            if 'Graph' in self._type:
                distances[vertex.value] = self.dijkstras(vertex.value)[1]
            else:
                distances[vertex] = self.dijkstras(vertex)[1]

        for vertex in distances:
            print(distances[vertex])

        self._graph = original_graph
        return distances