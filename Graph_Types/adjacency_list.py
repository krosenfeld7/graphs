"""The AdjacencyList class implements a simple adjacency list. This Adjacency List supports
   multiple edges between each vertex and can be directed or undirected. This class supports
   common graph operations such as union, intersection, difference and join.
"""

from copy import deepcopy
from collections import Counter
from .graph_exceptions import *


class AdjacencyList:
    
    def __init__(self, directed=True, multiple_edges=False):
        self.adjacency_list = {}
        self.vertices = set()
        self.directed = directed
        self.multiple_edges = multiple_edges

    def get_start_vertex(self):
        """

        Returns
        -------
        vertex
            a random vertex from this Adjacency List

        """
        return min(self.adjacency_list.keys())

    def verify_vertex_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is present in this Adjacency List

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
            vertex to verify is present in this Adjacency List

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex does exist

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
                return [node, [temp_vertex for temp_vertex in self.adjacency_list[node]]]

        # Unreachable
        return None

    def add_vertex(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex value to add to this Adjacency List

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex already exists (see verify_vertex_not_present())

        Returns
        -------
        bool
            if the new vertex was added successfully

        """
        self.verify_vertex_not_present(vertex)
        self.adjacency_list[vertex] = []
        self.vertices.add(vertex)
        
        return True
        
    def remove_vertex(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex value to remove from this Adjacency List

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see verify_vertex_present())

        Returns
        -------
        bool
            if the vertex was removed successfully

        """
        self.verify_vertex_present(vertex)
        del self.adjacency_list[vertex]
        self.vertices.discard(vertex)

        self._update_edges()
        
        return True
    
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
        
        temp_list = self.adjacency_list[vertex1]
        
        if not self.multiple_edges:
            for i in range(len(temp_list)):
                if temp_list[i][0] == vertex2:
                    raise NeighborAlreadyExistsError(f"Neighbor: {vertex2}: "
                                                     f"already present for vertex: {vertex1}")

        if not self.directed and vertex1 != vertex2:
            self.adjacency_list[vertex2].append([vertex1, weight])

        self.adjacency_list[vertex1].append([vertex2, weight])

        return True
    
    def remove_edge(self, vertex1, vertex2, weight=None):
        """
        
        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to remove
        vertex2 : int, string, etc.
            target of edge to remove
        weight : int
            the weight of the edge to remove

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

        original_list = deepcopy(self.adjacency_list[vertex1])
        temp_list = sorted([[edge[0], 0] if edge[1] is None
                            else edge for edge in self.adjacency_list[vertex1]],
                           key=lambda x: x[1], reverse=True)
        target = None

        for i in range(len(temp_list)):
            if weight is not None and temp_list[i][0] == vertex2 and temp_list[i][1] == weight:
                target = [vertex2, weight]
                break
            elif weight is None and temp_list[i][0] == vertex2:
                target = [vertex2, temp_list[i][1]]
                break

        if not target and weight is None:
            raise NeighborDoesNotExistError(f"Neighbor: {vertex2}: not present for vertex: {vertex1}")
        elif not target:
            raise NeighborDoesNotExistError(
                f"Neighbor: {vertex2} with weight: {weight}, not present for vertex: {vertex1}")
        else:
            if not self.directed:
                self.adjacency_list[vertex2].remove([vertex1, None if target[1] == 0 else target[1]])

            if target in original_list:
                original_list.remove(target)
            else:
                original_list.remove([target[0], None if target[1] == 0 else target[1]])
            self.adjacency_list[vertex1] = original_list

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
        if vertex1 not in self.adjacency_list:
            return False

        for i in range(len(self.adjacency_list[vertex1])):
            if self.adjacency_list[vertex1][i][0] == vertex2:
                return True

        return False

    def _update_edges(self):
        """

        Helper function. Removes edges to phantom vertices

        """
        for vertex in self.adjacency_list.keys():
            for i in range(len(self.adjacency_list[vertex])):
                if self.adjacency_list[vertex][i][0] not in self.adjacency_list.keys():
                    del self.adjacency_list[vertex][i]

    def empty(self):
        """
        
        Returns
        -------
        true
            if this Adjacency List is empty

        """
        return len(self.adjacency_list) == 0

    def union(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the union with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the union of the Adjacency Lists

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List union can only be performed on Adjacency Lists")

        if not self.multiple_edges:
            for vertex in self.adjacency_list.keys():
                if vertex in other.adjacency_list:
                    temp_list = self.adjacency_list[vertex]
                    temp_list.extend(other.adjacency_list[vertex])
                    temp_set = set(tuple(edge) for edge in temp_list)
                    temp_list = [list(edge) for edge in temp_set]
                    self.adjacency_list[vertex] = temp_list

            for vertex in other.adjacency_list.keys():
                if vertex not in self.adjacency_list:
                    self.adjacency_list[vertex] = other.adjacency_list[vertex]
                    temp_set = set(tuple(edge) for edge in self.adjacency_list[vertex])
                    self.adjacency_list[vertex] = [list(edge) for edge in temp_set]
        else:
            for vertex in self.adjacency_list.keys():
                if vertex in other.adjacency_list:
                    self.adjacency_list[vertex].extend(other.adjacency_list[vertex])

            for vertex in other.adjacency_list.keys():
                if vertex not in self.adjacency_list:
                    self.adjacency_list[vertex] = other.adjacency_list[vertex]

        self.vertices = set(self.adjacency_list.keys())
        return self

    def intersection(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the intersection with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the intersection of the Adjacency Lists

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List intersection can only be performed on Adjacency Lists")

        list_copy = deepcopy(self.adjacency_list)

        for vertex in list_copy.keys():
            if vertex not in other.adjacency_list:
                del self.adjacency_list[vertex]

        if not self.multiple_edges:
            for vertex in self.adjacency_list.keys():
                if vertex in other.adjacency_list:
                    self.adjacency_list[vertex] = \
                        [edge for edge in self.adjacency_list[vertex] if edge in other.adjacency_list[vertex]]
        elif not other.multiple_edges:
            for vertex in self.adjacency_list.keys():
                if vertex in other.adjacency_list:
                    temp_set = set(tuple(edge)
                                   for edge in other.adjacency_list[vertex] if edge in self.adjacency_list[vertex])
                    self.adjacency_list[vertex] = [list(edge) for edge in temp_set]
        else:
            for vertex in self.adjacency_list.keys():
                if vertex in other.adjacency_list:
                    self.adjacency_list[vertex] = \
                        [list(edge) for edge in
                         ((Counter([tuple(edge) for edge in self.adjacency_list[vertex]]) &
                           Counter([tuple(edge) for edge in other.adjacency_list[vertex]])).elements())]

        self.vertices = set(self.adjacency_list.keys())
        return self

    def difference(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the difference with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the difference between the Adjacency Lists

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List difference can only be performed on Adjacency Lists")

        list_copy = deepcopy(self.adjacency_list)

        for vertex in list_copy.keys():
            if vertex in other.adjacency_list:
                del self.adjacency_list[vertex]

        self._update_edges()
        self.vertices = set(self.adjacency_list.keys())
        return self

    def set_directed(self, directed):
        """

        Parameters
        ----------
        directed : bool
            field indicating if AdjacencyList will be updated to directed or not

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
        name_string += "Multi-Edged " if self.multiple_edges else ""
        name_string += "Adjacency "
        name_string += "List"

        return name_string

    def __add__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the join with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the join of the Adjacency Lists as a new Adjacency List

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List join can only be performed on Adjacency Lists")

        list_copy = deepcopy(self.adjacency_list)
        other_copy = deepcopy(other.adjacency_list)

        for vertex in other_copy.keys():
            if vertex not in list_copy:
                if not self.multiple_edges:
                    temp_set = set(tuple(edge) for edge in other_copy[vertex])
                    temp_list = [list(edge) for edge in temp_set]
                    list_copy[vertex] = temp_list
                else:
                    list_copy[vertex] = other.adjacency_list[vertex]

        for vertex in self.adjacency_list.keys():
            for node in other_copy.keys():
                if vertex != node:
                    if not self.is_neighbor(vertex, node):
                        list_copy[vertex].append([node, None])
                    if not self.directed and not self.is_neighbor(node, vertex):
                        list_copy[node].append([vertex, None])
                else:
                    if not self.multiple_edges:
                        temp_list = list_copy[vertex]
                        temp_list.extend(other.adjacency_list[vertex])
                        temp_set = set(tuple(edge) for edge in temp_list)
                        temp_list = [list(edge) for edge in temp_set]
                        list_copy[vertex] = temp_list
                    else:
                        list_copy[vertex].extend(other.adjacency_list[vertex])

        adjacency_list = AdjacencyList(self.directed, self.multiple_edges)
        adjacency_list.adjacency_list = list_copy
        adjacency_list.vertices = set(adjacency_list.adjacency_list.keys())
        return adjacency_list

    def __iadd__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the join with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the join of the Adjacency Lists

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List join can only be performed on Adjacency Lists")

        list_copy = deepcopy(self.adjacency_list)

        for vertex in other.adjacency_list.keys():
            if vertex not in list_copy:
                if not self.multiple_edges:
                    temp_set = set(tuple(edge) for edge in other.adjacency_list[vertex])
                    temp_list = [list(edge) for edge in temp_set]
                    list_copy[vertex] = temp_list
                else:
                    list_copy[vertex] = other.adjacency_list[vertex]

        for vertex in self.adjacency_list.keys():
            for node in other.adjacency_list.keys():
                if vertex != node:
                    if not self.is_neighbor(vertex, node):
                        list_copy[vertex].append([node, None])
                    if not self.directed and not self.is_neighbor(node, vertex):
                        list_copy[node].append([vertex, None])
                else:
                    if not self.multiple_edges:
                        temp_list = list_copy[vertex]
                        temp_list.extend(other.adjacency_list[vertex])
                        temp_set = set(tuple(edge) for edge in temp_list)
                        temp_list = [list(edge) for edge in temp_set]
                        list_copy[vertex] = temp_list
                    else:
                        list_copy[vertex].extend(other.adjacency_list[vertex])

        self.adjacency_list = list_copy
        self.vertices = set(self.adjacency_list.keys())
        return self

    def __sub__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the difference with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the difference between the Adjacency Lists as a new Adjacency List

        """
        if not isinstance(other, AdjacencyList):
            raise AdjacencyListOperationError("Adjacency List difference can only be performed on Adjacency Lists")

        list_copy = deepcopy(self.adjacency_list)

        for vertex in self.adjacency_list.keys():
            if vertex in other.adjacency_list:
                del list_copy[vertex]

        self._update_edges()

        adjacency_list = AdjacencyList(self.directed, self.multiple_edges)
        adjacency_list.adjacency_list = list_copy
        adjacency_list.vertices = set(adjacency_list.adjacency_list.keys())
        return adjacency_list

    def __isub__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to find the difference with

        Raises
        ------
        AdjacencyListOperationError
            if other is not an Adjacency List

        Returns
        -------
        AdjacencyList
            the difference between the Adjacency Lists (see difference())

        """
        return self.difference(other)

    def __eq__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, AdjacencyList):
            return False
        
        if self.directed != other.directed:
            return False
        
        if len(self.adjacency_list) != len(other.adjacency_list):
            return False
        
        for key in other.adjacency_list.keys():
            if key in self.adjacency_list:
                if self.adjacency_list[key] != other.adjacency_list[key]:
                    return False
            else:
                return False

        return True

    def __ne__(self, other):
        """

        Parameters
        ----------
        other : AdjacencyList
            the other Adjacency List to compare

        Returns
        -------
        bool
            true if other is not equal to self

        """
        return not self == other

    def _vertex_string(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            the vertex to construct a string for

        Returns
        -------
        string
            all neighbors and weights for the given vertex

        """
        temp_list = sorted([[edge[0], 0] if edge[1] is None else edge for edge in self.adjacency_list[vertex]],
                           key=lambda x: (x[0], x[1]))
        temp_list = [[edge[0], None] if edge[1] == 0 else edge for edge in temp_list]
        return f"{temp_list}"

    def __str__(self):
        """

        Returns
        -------
        string
            this Adjacency List as a string

        """
        out_string = self.name() + ":\n"
        out_dict = dict(sorted(self.adjacency_list.items()))
        for vertex in out_dict.keys():
            out_string += f"{vertex}: "
            if len(self.adjacency_list[vertex]) == 0:
                out_string += f"No neighbors\n"
            else:
                out_string += f"{self._vertex_string(vertex)}\n"
        
        if self.empty():
            out_string += "Empty Adjacency List\n"
        
        return out_string
