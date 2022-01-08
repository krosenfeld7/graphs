

from Graph_Algorithms.algorithm_exceptions import *
from Graph_Types.graph_exceptions import *
from Graph_Util.conversions import Conversions
from sys import maxsize
from math import inf


class Cuts:

    def __init__(self, graph=None):
        self._graph = graph
        self._type = type(self._graph).__name__
        if self._type not in ["UnweightedGraph", "WeightedGraph", "AdjacencyList", "AdjacencyMatrix"]:
            raise UnsupportedGraphTypeError(f"Invalid graph type: {self._type}")

        self._iterations = 0

    def _get_neighbors(self, node):
        if self._type == 'UnweightedGraph':
            return node.get_neighbors()
        elif self._type == 'WeightedGraph':
            return [neighbor[0] for neighbor in sorted(node.get_neighbors(), key=lambda neighbor: neighbor[1])]
        elif self._type == 'AdjacencyList':
            return [neighbor[0] for neighbor in sorted([[neighbor[0], -maxsize if neighbor[1] is None else
            neighbor[1]] for neighbor in self._graph.adjacency_list[node]], key=lambda neighbor: (neighbor[1],
                                                                                                  neighbor[0]))]
        elif self._type == 'AdjacencyMatrix':
            neighbors = []
            for i in range(len(self._graph.adjacency_matrix[self._graph.vertices[node]])):
                if self._graph.adjacency_matrix[self._graph.vertices[node]][i] != 0:
                    vertex2 = list(self._graph.vertices.keys())[list(self._graph.vertices.values()).index(i)]
                    tgt_weight = self._graph.adjacency_matrix[self._graph.vertices[node], self._graph.vertices[vertex2]]
                    if tgt_weight == 1:
                        tgt_weight = None
                    else:
                        tgt_weight = tgt_weight - 2 if tgt_weight > 0 else tgt_weight
                    neighbors.append([vertex2, tgt_weight])

            return [neighbor[0] for neighbor in sorted([[neighbor[0], -maxsize if neighbor[1] is None else
            neighbor[1]] for neighbor in neighbors], key=lambda neighbor: (neighbor[1], neighbor[0]))]

    def _articulation_recurse(self, vertex, visited, points, parent, low, seen):
        children = 0
        vertex_value = vertex.value if 'Graph' in self._type else vertex

        visited.append(vertex_value)

        seen[vertex_value] = self._iterations
        low[vertex_value] = self._iterations
        self._iterations += 1

        neighbors = self._get_neighbors(vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                parent[neighbor] = vertex_value
                children += 1
                if 'Graph' in self._type:
                    neighbor = self._graph.get_vertex(neighbor)

                self._articulation_recurse(neighbor, visited, points, parent, low, seen)
                if 'Graph' in self._type:
                    neighbor = neighbor.value

                low[vertex_value] = min(low[neighbor], low[vertex_value])

                if vertex_value not in parent and children > 1:
                    points.append(vertex_value)

                if vertex_value in parent and low[neighbor] >= seen[vertex_value]:
                    points.append(vertex_value)

            elif neighbor != parent[vertex_value]:
                low[vertex_value] = min(low[vertex_value], seen[neighbor])

    def articulation_points(self):
        if self._graph.directed:
            self._graph = Conversions.directed_to_undirected(self._graph)
        
        visited = []
        seen = dict()
        low = dict()
        parent = dict()

        for vertex in self._graph.vertices:
            vertex_value = vertex.value if 'Graph' in self._type else vertex
            seen[vertex_value] = inf
            low[vertex_value] = inf
            parent[vertex_value] = -1

        points = []

        for vertex in self._graph.vertices:
            if ('Graph' in self._type and vertex.value not in visited) or vertex not in visited:
                self._articulation_recurse(vertex, visited, points, parent, low, seen)

        return sorted(list(set(points)))

    def _bridges_recurse(self, vertex, visited, bridges, parent, low, seen):
        children = 0
        vertex_value = vertex.value if 'Graph' in self._type else vertex

        visited.append(vertex_value)

        seen[vertex_value] = self._iterations
        low[vertex_value] = self._iterations
        self._iterations += 1

        neighbors = self._get_neighbors(vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                parent[neighbor] = vertex_value
                children += 1
                if 'Graph' in self._type:
                    neighbor = self._graph.get_vertex(neighbor)

                self._bridges_recurse(neighbor, visited, bridges, parent, low, seen)
                if 'Graph' in self._type:
                    neighbor = neighbor.value

                low[vertex_value] = min(low[neighbor], low[vertex_value])

                if low[neighbor] > seen[vertex_value]:
                    bridges.append([vertex_value, neighbor])

            elif neighbor != parent[vertex_value]:
                low[vertex_value] = min(low[vertex_value], seen[neighbor])

    def bridges(self):
        if self._graph.directed:
            self._graph = Conversions.directed_to_undirected(self._graph)

        if self._graph.directed:
            self._graph = Conversions.directed_to_undirected(self._graph)

        visited = []
        seen = dict()
        low = dict()
        parent = dict()

        for vertex in self._graph.vertices:
            vertex_value = vertex.value if 'Graph' in self._type else vertex
            seen[vertex_value] = inf
            low[vertex_value] = inf
            parent[vertex_value] = -1

        bridges = []

        for vertex in self._graph.vertices:
            if ('Graph' in self._type and vertex.value not in visited) or vertex not in visited:
                self._bridges_recurse(vertex, visited, bridges, parent, low, seen)

        return bridges