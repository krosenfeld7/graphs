

from Graph_Algorithms.algorithm_exceptions import *
from Graph_Algorithms.shortest_paths import ShortestPaths
from collections import Counter
from sys import maxsize


class Cycles:

    def __init__(self, graph=None):
        self._graph = graph
        self._type = type(self._graph).__name__
        if self._type not in ["UnweightedGraph", "WeightedGraph", "AdjacencyList", "AdjacencyMatrix"]:
            raise UnsupportedGraphTypeError(f"Invalid graph type: {self._type}")

    def _get_neighbors(self, node):
        if self._type == 'UnweightedGraph':
            return node.get_neighbors()
        elif self._type == 'WeightedGraph':
            return sorted([neighbor[0] for neighbor in node.get_neighbors()])
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

    def _undirected_graph_cycle_recurse(self, node, visited, parent=None):
        visited.append(node.value)
        neighbors = self._get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                neighbor = self._graph.get_vertex(neighbor)
                if self._undirected_graph_cycle_recurse(neighbor, visited, node):
                    return True
                if neighbor in visited:
                    visited.remove(neighbor)
            elif parent and parent.value != neighbor:
                visited.append(neighbor)
                return True
            elif self._graph.multiple_edges:
                if (isinstance(node.neighbors[neighbor], list) and len(node.neighbors[neighbor]) > 1) or \
                        (isinstance(node.neighbors[neighbor], int) and node.neighbors[neighbor] > 1) or \
                        node.value == neighbor:
                    visited.append(neighbor)
                    return True

        return False

    def _directed_graph_cycle_recurse(self, node, visited, recursion_stack):
        visited.append(node.value)
        recursion_stack.append(node.value)
        neighbors = self._get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                neighbor = self._graph.get_vertex(neighbor)
                if self._directed_graph_cycle_recurse(neighbor, visited, recursion_stack):
                    return True
                if neighbor in visited:
                    visited.remove(neighbor)
            elif neighbor in recursion_stack:
                visited.append(neighbor)
                return True

        recursion_stack.remove(node.value)
        return False

    def _graph_cycle(self):
        visited = []
        recursion_stack = []

        for node in sorted(self._graph.vertices, key=lambda x: x.value):
            if node.value not in visited:
                if not self._graph.directed:
                    if self._undirected_graph_cycle_recurse(node, visited):
                        visited = visited[visited.index(visited[-1]):]
                        return [True, visited]
                else:
                    if self._directed_graph_cycle_recurse(node, visited, recursion_stack):
                        visited = visited[visited.index(visited[-1]):]
                        return [True, visited]

        return [False, [None]]

    def _undirected_adjacency_cycle_recurse(self, node, visited, parent=None):
        visited.append(node)
        neighbors = self._get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                if self._undirected_adjacency_cycle_recurse(neighbor, visited, node):
                    return True
                if neighbor in visited:
                    visited.remove(neighbor)
            elif parent and parent != neighbor:
                visited.append(neighbor)
                return True
            elif self._graph.multiple_edges:
                temp_node = self._graph.get_vertex(node)
                temp_node[1] = [temp[0] for temp in temp_node[1]]
                if Counter(temp_node[1])[neighbor] > 1 or \
                        node == neighbor:
                    visited.append(neighbor)
                    return True

        return False

    def _directed_adjacency_cycle_recurse(self, node, visited, recursion_stack):
        visited.append(node)
        recursion_stack.append(node)
        neighbors = self._get_neighbors(node)

        for neighbor in neighbors:
            if neighbor not in visited:
                if self._directed_adjacency_cycle_recurse(neighbor, visited, recursion_stack):
                    return True
                if neighbor in visited:
                    visited.remove(neighbor)
            elif neighbor in recursion_stack:
                visited.append(neighbor)
                return True

        recursion_stack.remove(node)
        return False

    def _adjacency_cycle(self):
        visited = []
        recursion_stack = []

        for node in sorted(self._graph.vertices):
            if node not in visited:
                if not self._graph.directed:
                    if self._undirected_adjacency_cycle_recurse(node, visited):
                        visited = visited[visited.index(visited[-1]):]
                        return [True, visited]
                else:
                    if self._directed_adjacency_cycle_recurse(node, visited, recursion_stack):
                        visited = visited[visited.index(visited[-1]):]
                        return [True, visited]

        return [False, None]

    def detect_cycle(self):
        if 'Graph' in self._type:
            return self._graph_cycle()
        else:
            return self._adjacency_cycle()

    def detect_negative_cycle(self):
        shortest_path = ShortestPaths(self._graph)
        distances = shortest_path.floyd_warshall()
        negative_cycle = False

        for vertex in distances:
            for path in distances[vertex]:
                if vertex == path[0] and path[1] < 0:
                    negative_cycle = True

        return negative_cycle

    def _verify_path(self, path, vertex):
        for path_vertex in path:
            if path_vertex == vertex:
                return False

        return True

    def _graph_adjacent_vertex_not_in_path(self, vertex, curr_index, path):
        return self._graph.get_vertex(path[curr_index - 1]).is_neighbor(vertex) and self._verify_path(path, vertex)

    def _graph_hamiltonian_cycle_recurse(self, path, curr_index):
        if curr_index == len(self._graph.vertices):
            return self._graph.get_vertex(path[curr_index - 1]).is_neighbor(path[0])

        for vertex in self._graph.vertices:
            if self._graph_adjacent_vertex_not_in_path(vertex.value, curr_index, path):
                path.append(vertex.value)

                if self._graph_hamiltonian_cycle_recurse(path, curr_index + 1):
                    return True

                path.remove(vertex.value)

        return False

    def _adjacency_adjacent_vertex_not_in_path(self, vertex, curr_index, path):
        return vertex not in [neighbor[0] for neighbor in self._graph.get_vertex(path[curr_index - 1])[1]] and \
               self._verify_path(path, vertex)

    def _adjacency_hamiltonian_cycle_recurse(self, path, curr_index):
        if curr_index == len(self._graph.vertices):
            return path[0] in [neighbor[0] for neighbor in self._graph.get_vertex(path[curr_index - 1])[1]]

        for vertex in self._graph.vertices:
            if self._adjacency_adjacent_vertex_not_in_path(vertex, curr_index, path):
                path.append(vertex)

                if self._adjacency_hamiltonian_cycle_recurse(path, curr_index + 1):
                    return True

                path.remove(vertex)

        return False

    def _graph_hamiltonian_cycle(self, start_node=None):
        path = [start_node.value]

        if not self._graph_hamiltonian_cycle_recurse(path, 1):
            return [False, None]

        path.append(path[0])
        return [True, path]

    def _adjacency_hamiltonian_cycle(self, start_node=None):
        path = [start_node]

        if not self._adjacency_hamiltonian_cycle_recurse(path, 1):
            return [False, None]

        path.append(path[0])
        return [True, path]

    def hamiltonian_cycle(self, start_node=None):
        start_node = self._graph.get_vertex(start_node) if start_node is not None else self._graph.get_start_vertex()

        if 'Graph' in self._type:
            return self._graph_hamiltonian_cycle(start_node)
        else:
            return self._adjacency_hamiltonian_cycle(start_node[0])
