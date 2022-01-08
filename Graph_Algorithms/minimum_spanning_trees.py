

from Graph_Algorithms.algorithm_exceptions import *
from Graph_Types.graph_exceptions import *
from sys import maxsize


class MSTs:

    def __init__(self, graph=None):
        self._graph = graph
        self._type = type(self._graph).__name__
        if self._type not in ["UnweightedGraph", "WeightedGraph", "AdjacencyList", "AdjacencyMatrix"]:
            raise UnsupportedGraphTypeError(f"Invalid graph type: {self._type}")

    def verify_root_node(self, start_node=None):
        if start_node:
            try:
                self._graph.verify_vertex_present(start_node)
                return start_node
            except VertexDoesNotExistError:
                raise InvalidMSTNodeError(f"Start Vertex: {start_node} not present in graph") from None
        else:
            return self._graph.get_start_vertex().value if 'Graph' in self._type else self._graph.get_start_vertex()

    def _min_weight_not_in_mst(self, weights, vertex_set):
        min_weight = maxsize
        min_vertex = None

        for vertex, weight in weights.items():
            if weight < min_weight and vertex in vertex_set:
                min_weight = weight
                min_vertex = vertex

        return min_vertex, min_weight

    def prims_mst(self, start_node=None):
        if self._graph.directed:
            raise UnsupportedGraphTypeError(f"This {self._graph.name()} is a directed graph. Prim's MST is "
                                            f"incompatible with directed graphs.")

        start_node = self.verify_root_node(start_node)
        weights = {}
        parent = {}
        vertex_set = set()
        mst = []
        min_cost = 0

        for vertex in self._graph.vertices:
            weights[vertex.value if not isinstance(vertex, int) else vertex] = maxsize
            vertex_set.add(vertex.value if not isinstance(vertex, int) else vertex)
            parent[vertex.value if not isinstance(vertex, int) else vertex] = None

        weights[start_node] = 0

        for i in self._graph.vertices:
            min_vertex, min_weight = self._min_weight_not_in_mst(weights, vertex_set)
            vertex_set.discard(min_vertex)

            if parent[min_vertex] is not None:
                mst.append([parent[min_vertex][0], min_vertex, parent[min_vertex][1]])

            for vertex in self._graph.vertices:
                if isinstance(vertex, int):
                    temp_weight = [neighbor[1] for neighbor in self._graph.get_vertex(vertex)[1] if
                                   neighbor[0] == min_vertex]
                    if len(temp_weight) > 0 and vertex in vertex_set and weights[vertex] > temp_weight[0]:
                        weights[vertex] = temp_weight[0]
                        parent[vertex] = [min_vertex, temp_weight[0]]
                else:
                    if vertex.is_neighbor(min_vertex) and vertex.value in vertex_set:
                        if isinstance(vertex.neighbors, set):
                            if weights[vertex.value] > 1:
                                weights[vertex.value] = 1
                                parent[vertex.value] = min_vertex
                        elif weights[vertex.value] > vertex.neighbors[min_vertex]:
                            weights[vertex.value] = vertex.neighbors[min_vertex]
                            parent[vertex.value] = [min_vertex, vertex.neighbors[min_vertex]]

        for edge in mst:
            min_cost += edge[2]

        return [min_cost, mst]

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

        edges = sorted(edges.items(), key=lambda x: x[1])
        edges = [[*edge[0], edge[1]] for edge in edges]
        return edges

    def _find_set(self, nodes, target):
        if nodes[target] == target:
            return target
        return self._find_set(nodes, nodes[target])

    def _union(self, nodes, rank, first, second):
        root1 = self._find_set(nodes, first)
        root2 = self._find_set(nodes, second)

        if rank[root1] > rank[root2]:
            nodes[root2] = root1
        elif rank[root1] < rank[root2]:
            nodes[root1] = root2
        else:
            nodes[root2] = root1
            rank[root1] += 1

    def kruskals_mst(self):
        if self._graph.directed:
            raise UnsupportedGraphTypeError(f"This {self._graph.name()} is a directed graph. Kruskal's MST is "
                                            f"incompatible with directed graphs.")
        edges = self._get_edges()
        nodes = []
        rank = [0] * len(self._graph.vertices)
        mst = []
        min_cost = 0

        for vertex in self._graph.vertices:
            nodes.append(vertex.value if 'Graph' in self._type else vertex)

        nodes.sort()

        while len(mst) < len(self._graph.vertices) - 1:
            if len(edges) == 0:
                break
            edge = edges.pop(0)
            first = self._find_set(nodes, edge[0])
            second = self._find_set(nodes, edge[1])

            if first != second:
                mst.append(edge)
                min_cost += edge[2]
                self._union(nodes, rank, first, second)

        return [min_cost, mst]

    def arborescence(self):
        if not self._graph.directed:
            raise UnsupportedGraphTypeError(f"This {self._graph.name()} is a undirected graph. Arborescence is "
                                            f"incompatible with undirected graphs.")

        raise AlgorithmNotImplementedError("Arborescence is unsupported")
