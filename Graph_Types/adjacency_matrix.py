"""The AdjacencyMatrix class implements a simple adjacency list. This Adjacency Matrix supports
   only unique edges between each vertex and can be directed or undirected. This class supports
   common graph operations such as union, intersection, difference and join. Note that this class
   does not support duplicate edges.
"""

from copy import deepcopy
import numpy as np
from .graph_exceptions import *


class AdjacencyMatrix:

    def __init__(self, directed=True, multiple_edges=False):
        self.adjacency_matrix = np.array([])
        self.vertices = {}
        self.directed = directed
        self.multiple_edges = False
        if multiple_edges:
            raise AdjacencyMatrixOperationError("Adjacency Matrices do not support multiple edges")

    def get_start_vertex(self):
        """

        Returns
        -------
        vertex
            a random vertex from this Adjacency Matrix

        """
        return min(self.vertices, key=self.vertices.get)

    def verify_vertex_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is present in this Adjacency Matrix

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist

        """
        if vertex not in self.vertices:
            raise VertexDoesNotExistError(f"Vertex: {vertex}: not present in graph")

    def verify_vertex_not_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is not present in this Adjacency Matrix

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex already exists

        """
        if vertex in self.vertices:
            raise VertexAlreadyExistsError(f"Vertex: {vertex}: already present in graph")

    def get_vertex(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to find

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see verify_vertex_present())

        """
        self.verify_vertex_present(vertex)

        for node in self.vertices:
            if node == vertex:
                temp_node = self.adjacency_matrix[self.vertices[node]]
                temp_neighbors = []
                for entry in range(len(temp_node)):
                    if temp_node[entry] != 0:
                        weight = temp_node[entry]
                        if weight == 1:
                            weight = None
                        else:
                            weight = weight - 2 if weight > 0 else weight
                        temp_neighbors.append([self.vertices[entry], weight])

                return [node, temp_neighbors]

        # Unreachable
        return None

    def add_vertex(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex value to add to this Adjacency Matrix

        Returns
        -------
        bool
            if the new vertex was added successfully

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex already exists (see verify_vertex_not_present())

        """
        self.verify_vertex_not_present(vertex)

        if self.empty():
            self.adjacency_matrix = np.array([[0] * 1] * 1)
            self.vertices[vertex] = len(self.vertices.keys())
        else:
            self.vertices[vertex] = len(self.vertices.keys())
            self.adjacency_matrix = np.insert(self.adjacency_matrix, self.vertices[vertex], values=0, axis=0)
            self.adjacency_matrix = np.insert(self.adjacency_matrix, self.vertices[vertex], values=0, axis=1)

        return True

    def remove_vertex(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex value to remove from this Adjacency Matrix

        Returns
        -------
        bool
            if the vertex was removed successfully

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see verify_vertex_present())

        """
        self.verify_vertex_present(vertex)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, self.vertices[vertex], axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, self.vertices[vertex], axis=1)
        del self.vertices[vertex]

        index = 0
        for key in self.vertices.keys():
            self.vertices[key] = index
            index += 1

        return True

    @staticmethod
    def update_weight(weight):
        """

        Parameters
        ----------
        weight : int.
            weight to map

        Returns
        -------
        int
            mapped weight

        """
        if weight is None:
            weight = 1
        elif weight >= 0:
            weight += 2

        return weight

    def add_edge(self, vertex1, vertex2, weight=None):
        """

        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to add
        vertex2 : int, string, etc.
            target of edge to add
        weight : int, optional
            weight of the edge to add. The default is None

        Raises
        ------
        VertexDoesNotExistError
            if the given vertices do not exist (see verify_vertex_present())
        NeighborAlreadyExistsError
            if the given edge already exists

        Returns
        -------
        bool
            True on success

        """
        self.verify_vertex_present(vertex1)
        self.verify_vertex_present(vertex2)

        if self.adjacency_matrix[self.vertices[vertex1], self.vertices[vertex2]] != 0:
            raise NeighborAlreadyExistsError(f"Neighbor: {vertex2}: already present for vertex: {vertex1}")

        weight = self.update_weight(weight)

        self.adjacency_matrix[self.vertices[vertex1], self.vertices[vertex2]] = weight

        if not self.directed and vertex1 != vertex2 and \
                self.adjacency_matrix[self.vertices[vertex2], self.vertices[vertex1]] == 0:
            self.adjacency_matrix[self.vertices[vertex2], self.vertices[vertex1]] = weight

        return True

    def remove_edge(self, vertex1, vertex2, weight=None):
        """

        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to add
        vertex2 : int, string, etc.
            target of edge to add
        weight : int
            will always be set to None for AdjacencyMatrices

        Raises
        ------
        VertexDoesNotExistError
            if the given vertices do not exist (see verify_vertex_present())
        NeighborDoesNotExistError
            if the given edge does not exist

        Returns
        -------
        bool
            True on success

         """
        self.verify_vertex_present(vertex1)
        self.verify_vertex_present(vertex2)

        if self.adjacency_matrix[self.vertices[vertex1], self.vertices[vertex2]] == 0:
            raise NeighborDoesNotExistError(f"Neighbor: {vertex2}: not present for vertex: {vertex1}")

        self.adjacency_matrix[self.vertices[vertex1], self.vertices[vertex2]] = 0

        if not self.directed and vertex1 != vertex2 and \
                self.adjacency_matrix[self.vertices[vertex2], self.vertices[vertex1]] != 0:
            self.adjacency_matrix[self.vertices[vertex2], self.vertices[vertex1]] = 0

        return True

    def is_neighbor(self, vertex1, vertex2):
        """

        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to check
        vertex2 : int, string, etc.
            target of edge to check

        Returns
        -------
        bool
            if vertex2 is a neighbor of vertex1

        """
        if self.adjacency_matrix[self.vertices[vertex1], self.vertices[vertex2]] != 0:
            return True

        return False

    def empty(self):
        """

        Returns
        -------
        bool
            if this Adjacency Matrix is empty

        """
        return len(self.vertices) == 0 and len(self.adjacency_matrix) == 0

    def set_directed(self, directed):
        """

        Parameters
        ----------
        directed : bool
            field indicating if AdjacencyMatrix will be updated to directed or not

        """
        self.directed = directed

    def name(self):
        """

        Returns
        -------
        string
            type name

        """
        name_string = "Directed " if self.directed else "Undirected "
        name_string += "Adjacency Matrix"

        return name_string

    def _transpose(self, other, direction=True):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to transpose vertices to
        direction : bool, optional
            the direction for mapping matrix indices
            - True = other --> self
            - False = self --> other

        Returns
        -------
        dict
            the transpose of the indices between self and other

        """
        transposed = {}

        if direction:
            for vertex in self.vertices:
                if vertex in other.vertices:
                    transposed[other.vertices[vertex]] = self.vertices[vertex]
        else:
            for vertex in other.vertices:
                if vertex in self.vertices:
                    transposed[self.vertices[vertex]] = other.vertices[vertex]

        return transposed

    def union(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the union with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the union of the Adjacency Matrices

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError("Adjacency Matrix union can only be performed on Adjacency Matrices")

        transposed = self._transpose(other, True)

        for vertex in other.vertices:
            if vertex not in self.vertices:
                self.add_vertex(vertex)
            transposed[other.vertices[vertex]] = self.vertices[vertex]

        for index, value in np.ndenumerate(other.adjacency_matrix):
            if self.adjacency_matrix[transposed[index[0]], transposed[index[1]]] == 0 and value != 0:
                self.adjacency_matrix[transposed[index[0]], transposed[index[1]]] = value
            elif value != 0 and value != 1:
                self.adjacency_matrix[transposed[index[0]], transposed[index[1]]] = \
                    min(self.adjacency_matrix[transposed[index[0]], transposed[index[1]]], value)

            if not self.directed and other.directed:
                if self.adjacency_matrix[transposed[index[1]], transposed[index[0]]] == 0 and \
                        other.adjacency_matrix[index[1], index[0]] != 0:
                    self.adjacency_matrix[transposed[index[1]], transposed[index[0]]] = \
                        other.adjacency_matrix[index[1], index[0]]
                elif other.adjacency_matrix[index[1], index[0]] != 0 and \
                        other.adjacency_matrix[index[1], index[0]] != 1:
                    self.adjacency_matrix[transposed[index[1]], transposed[index[0]]] = \
                        min(self.adjacency_matrix[transposed[index[1]], transposed[index[0]]],
                            other.adjacency_matrix[index[1], index[0]])

        return self

    def intersection(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the intersection with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the intersection of the Adjacency Matrices

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError(
                "Adjacency Matrix intersection can only be performed on Adjacency Matrices")

        vertices_copy = deepcopy(self.vertices)
        for vertex in vertices_copy.keys():
            if vertex not in other.vertices:
                self.remove_vertex(vertex)

        transposed = self._transpose(other, False)

        for vertex in self.vertices:
            if vertex not in other.vertices:
                self.remove_vertex(vertex)

        for index, value in np.ndenumerate(self.adjacency_matrix):
            if other.adjacency_matrix[transposed[index[0]], transposed[index[1]]] != 0 and value != 0:
                if other.adjacency_matrix[transposed[index[0]], transposed[index[1]]] != 1:
                    self.adjacency_matrix[index[0], index[1]] = \
                        min(other.adjacency_matrix[transposed[index[0]], transposed[index[1]]], value)
            else:
                self.adjacency_matrix[index[0], index[1]] = 0

            if not self.directed and other.directed:
                if other.adjacency_matrix[transposed[index[1]], transposed[index[0]]] != 0 and \
                        self.adjacency_matrix[index[1], index[0]] != 0:
                    if other.adjacency_matrix[transposed[index[1]], transposed[index[0]]] != 1:
                        self.adjacency_matrix[index[1], index[0]] = \
                            min(other.adjacency_matrix[transposed[index[1]], transposed[index[0]]],
                                self.adjacency_matrix[index[1], index[0]])
                else:
                    self.adjacency_matrix[index[1], index[0]] = 0

        return self

    def difference(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the difference with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the difference between the Adjacency Matrices

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError(
                "Adjacency Matrix difference can only be performed on Adjacency Matrices")

        vertices_copy = deepcopy(self.vertices)
        for vertex in vertices_copy.keys():
            if vertex in other.vertices.keys():
                self.remove_vertex(vertex)

        return self

    def __add__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the join with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the join of the Adjacency Matrices as a new Adjacency Matrix

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError(
                "Adjacency Matrix join can only be performed on Adjacency Matrices")

        transposed = self._transpose(other, True)

        adjacency_matrix = AdjacencyMatrix(self.directed)
        adjacency_matrix.adjacency_matrix = deepcopy(self.adjacency_matrix)
        adjacency_matrix.vertices = deepcopy(self.vertices)

        for vertex in other.vertices:
            if vertex not in self.vertices:
                adjacency_matrix.add_vertex(vertex)
            transposed[other.vertices[vertex]] = adjacency_matrix.vertices[vertex]

        for index, value in np.ndenumerate(other.adjacency_matrix):
            if adjacency_matrix.adjacency_matrix[transposed[index[0]], transposed[index[1]]] == 0 and value != 0:
                adjacency_matrix.adjacency_matrix[transposed[index[0]], transposed[index[1]]] = value
            elif value != 0 and value != 1:
                adjacency_matrix.adjacency_matrix[transposed[index[0]], transposed[index[1]]] = \
                    min(adjacency_matrix.adjacency_matrix[transposed[index[0]], transposed[index[1]]], value)

            if not adjacency_matrix.directed and other.directed:
                if adjacency_matrix.adjacency_matrix[transposed[index[1]], transposed[index[0]]] == 0 and \
                        other.adjacency_matrix[index[1], index[0]] != 0:
                    adjacency_matrix.adjacency_matrix[transposed[index[1]], transposed[index[0]]] = \
                        other.adjacency_matrix[index[1], index[0]]
                elif other.adjacency_matrix[index[1], index[0]] != 0 and \
                        other.adjacency_matrix[index[1], index[0]] != 1:
                    adjacency_matrix.adjacency_matrix[transposed[index[1]], transposed[index[0]]] = \
                        min(adjacency_matrix.adjacency_matrix[transposed[index[1]], transposed[index[0]]],
                            other.adjacency_matrix[index[1], index[0]])

        for vertex in self.vertices:
            for node in other.vertices:
                if vertex != node:
                    if not adjacency_matrix.is_neighbor(vertex, node):
                        adjacency_matrix.add_edge(vertex, node)
                    if not adjacency_matrix.directed and not adjacency_matrix.is_neighbor(node, vertex):
                        adjacency_matrix.add_edge(node, vertex)

        return adjacency_matrix

    def __iadd__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the join with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the join of the Adjacency Matrices

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError(
                "Adjacency Matrix join can only be performed on Adjacency Matrices")

        temp_copy = deepcopy(self.vertices)
        self.union(other)

        for vertex in temp_copy.keys():
            for node in other.vertices:
                if vertex != node:
                    if not self.is_neighbor(vertex, node):
                        self.add_edge(vertex, node)
                    if not self.directed and not self.is_neighbor(node, vertex):
                        self.add_edge(node, vertex)

        return self

    def __sub__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the difference with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix

        Returns
        -------
        AdjacencyMatrix
            the difference between the Adjacency Matrices as a new Adjacency Matrix

        """
        if not isinstance(other, AdjacencyMatrix):
            raise AdjacencyMatrixOperationError(
                "Adjacency Matrix difference can only be performed on Adjacency Matrices")

        adjacency_matrix = AdjacencyMatrix(self.directed)
        adjacency_matrix.vertices = deepcopy(self.vertices)
        adjacency_matrix.adjacency_matrix = deepcopy(self.adjacency_matrix)

        for vertex in self.vertices.keys():
            if vertex in other.vertices.keys():
                adjacency_matrix.remove_vertex(vertex)

        return adjacency_matrix

    def __isub__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to find the difference with

        Raises
        ------
        AdjacencyMatrixOperationError
            if other is not an Adjacency Matrix (see difference())

        Returns
        -------
        AdjacencyMatrix
            the difference between the Adjacency Matrices

        """
        return self.difference(other)

    def __eq__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, AdjacencyMatrix):
            return False

        if not (self.adjacency_matrix == other.adjacency_matrix).all():
            return False

        if self.directed != other.directed:
            return False

        return True

    def __ne__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyMatrix
            the other Adjacency Matrix to compare

        Returns
        -------
        bool
            true if other is not equal to self

        """
        return not self == other

    def __str__(self):
        """

        Returns
        -------
        string
            this Adjacency Matrix as a string

        """
        out_string = self.name() + ":\n"

        for vertex in sorted(self.vertices.keys()):
            out_string += f"{vertex}: "
            vertex_list = []
            for i in range(len(self.adjacency_matrix[self.vertices[vertex]])):
                if self.adjacency_matrix[self.vertices[vertex]][i] != 0:
                    vertex2 = list(self.vertices.keys())[list(self.vertices.values()).index(i)]
                    tgt_weight = self.adjacency_matrix[self.vertices[vertex], self.vertices[vertex2]]
                    if tgt_weight == 1:
                        tgt_weight = None
                    else:
                        tgt_weight = tgt_weight - 2 if tgt_weight > 0 else tgt_weight
                    vertex_list.append([vertex2, tgt_weight])

            out_string += \
                f"{'No Neighbors' if len(vertex_list) == 0 else sorted(vertex_list, key = lambda x : (x[0], x[1]))}\n"

        if self.empty():
            out_string += "Empty Adjacency Matrix\n"

        return out_string
