

from Graph_Algorithms.algorithm_exceptions import *
from Graph_Types.graph_exceptions import *
from Graph_Algorithms.cycles import Cycles
from sys import maxsize


class Traversals:

    def __init__(self, graph=None):
        self._graph = graph
        self._type = type(self._graph).__name__
        if self._type not in ["UnweightedGraph", "WeightedGraph", "AdjacencyList", "AdjacencyMatrix"]:
            raise UnsupportedGraphTypeError(f"Invalid graph type: {self._type}")

    def _verify_root_node(self, start_node=None):
        if start_node:
            try:
                self._graph.verify_vertex_present(start_node)
                return self._graph.get_vertex(start_node) if 'Graph' in self._type else start_node
            except VertexDoesNotExistError:
                raise InvalidTraversalNodeError(f"Start Vertex: {start_node} not present in graph") from None
        else:
            return self._graph.get_start_vertex()

    def _verify_target_node(self, target_node):
        try:
            self._graph.verify_vertex_present(target_node)
        except VertexDoesNotExistError:
            raise InvalidTraversalNodeError(f"Target Vertex: {target_node} not present in graph") from None

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

    def bft(self, start_node=None):
        start_node = self._verify_root_node(start_node)
        visited = []

        if 'Graph' in self._type:
            visited = [start_node.value]
            neighbors = self._get_neighbors(start_node)

            while neighbors:
                temp_node = neighbors.pop(0)
                if temp_node not in visited:
                    visited.append(temp_node)
                    temp_node = self._graph.get_vertex(temp_node)
                    neighbors.extend(self._get_neighbors(temp_node))

            if len(visited) != len(self._graph.vertices):
                raise IncompleteTraversalError(f"Incomplete breadth first traversal of graph: {visited}, "
                                               f"vertex {visited[-1]} is disconnected")
        elif 'Adjacency' in self._type:
            visited = [start_node]
            neighbors = self._get_neighbors(start_node)

            while neighbors:
                temp_node = neighbors.pop(0)
                if temp_node not in visited:
                    visited.append(temp_node)
                    neighbors.extend(self._get_neighbors(temp_node))

            if self._type == 'AdjacencyList':
                if len(visited) != len(self._graph.adjacency_list.keys()):
                    raise IncompleteTraversalError(f"Incomplete breadth first traversal of adjacency list: {visited}, "
                                                   f"vertex {visited[-1]} not found")
            elif len(visited) != len(self._graph.vertices):
                raise IncompleteTraversalError(f"Incomplete breadth first traversal of adjacency matrix: {visited}, "
                                               f"vertex {visited[-1]} is disconnected")
        return visited

    def bfs(self, target_node, start_node=None):
        start_node = self._verify_root_node(start_node)
        self._verify_target_node(target_node)
        visited = []

        if 'Graph' in self._type:
            visited = [start_node.value]
            if start_node.value == target_node:
                return visited

            neighbors = self._get_neighbors(start_node)

            while neighbors:
                temp_node = neighbors.pop(0)
                if temp_node not in visited:
                    visited.append(temp_node)
                    if temp_node == target_node:
                        return visited
                    temp_node = self._graph.get_vertex(temp_node)
                    neighbors.extend(self._get_neighbors(temp_node))

        elif 'Adjacency' in self._type:
            visited = [start_node]
            if start_node == target_node:
                return visited

            neighbors = self._get_neighbors(start_node)

            while neighbors:
                temp_node = neighbors.pop(0)
                if temp_node not in visited:
                    visited.append(temp_node)
                    if temp_node == target_node:
                        return visited
                    neighbors.extend(self._get_neighbors(temp_node))

        return visited

    def _dft_recurse(self, node, visited):
        visited.append(node.value if 'Graph' in self._type else node)
        neighbors = self._get_neighbors(node)

        while neighbors:
            temp_node = neighbors.pop(0)
            if temp_node not in visited:
                if 'Graph' in self._type:
                    temp_node = self._graph.get_vertex(temp_node)

                self._dft_recurse(temp_node, visited)

    def dft(self, start_node=None):
        start_node = self._verify_root_node(start_node)
        visited = []
        self._dft_recurse(start_node, visited)

        if 'Graph' in self._type and len(visited) != len(self._graph.vertices):
            raise IncompleteTraversalError(f"Incomplete depth first traversal of graph: {visited}, "
                                           f"vertex {visited[-1]} is disconnected")
        elif self._type == 'AdjacencyList' and len(visited) != len(self._graph.adjacency_list.keys()):
            raise IncompleteTraversalError(f"Incomplete depth first traversal of adjacency list: {visited}, "
                                           f"vertex {visited[-1]} not found")
        elif self._type == 'AdjacencyMatrix' and len(visited) != len(self._graph.vertices):
            raise IncompleteTraversalError(f"Incomplete depth first traversal of adjacency matrix: {visited}, "
                                           f"vertex {visited[-1]} is disconnected")
        return visited

    def _dfs_recurse(self, node, target, visited):
        visited.append(node.value if 'Graph' in self._type else node)

        if ('Graph' in self._type and node.value == target.value) or node == target:
            return visited

        neighbors = self._get_neighbors(node)
        while neighbors:
            temp_node = neighbors.pop(0)
            if temp_node not in visited:
                if 'Graph' in self._type:
                    temp_node = self._graph.get_vertex(temp_node)

                if self._dfs_recurse(temp_node, target, visited):
                    return True

    def dfs(self, target_node, start_node=None):
        start_node = self._verify_root_node(start_node)
        self._verify_target_node(target_node)
        visited = []
        self._dfs_recurse(start_node, target_node, visited)

        return visited

    def _topological_recurse(self, node, visited, stack):
        visited.append(node.value if 'Graph' in self._type else node)
        neighbors = self._get_neighbors(node)

        while neighbors:
            temp_node = neighbors.pop(0)
            if temp_node not in visited:
                if 'Graph' in self._type:
                    temp_node = self._graph.get_vertex(temp_node)

                self._topological_recurse(temp_node, visited, stack)

        if ('Graph' in self._type and node.value not in stack) or (node not in stack):
            stack.append(node.value if 'Graph' in self._type else node)

    def topological(self):
        if not self._graph.directed:
            raise UnsupportedGraphTypeError(f"This {self._graph.name()} is an undirected graph. Topological Sort is "
                                            f"incompatible with undirected graphs.")
        cycle = Cycles(self._graph)

        if cycle.detect_cycle()[0]:
            raise UnsupportedGraphTypeError(f"This {self._graph.name()} is a cyclic graph. Topological Sort is "
                                            f"incompatible with cyclic graphs.")
        visited = []
        stack = []

        for vertex in self._graph.vertices:
            self._topological_recurse(vertex, visited, stack)

        return stack[::-1]
