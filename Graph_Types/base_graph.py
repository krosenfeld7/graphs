"""The BaseGraph class implements a basic graph without edges.
   Unweighted and Weighted Graphs both inherit the BaseGraph class.
"""

from .base_graph_node import BaseGraphNode
from .graph_exceptions import *
from copy import deepcopy


class BaseGraph:
    
    def __init__(self):
        self.vertices = set()
        self.directed = False
        self.multiple_edges = False
        self.default_weight = 0

    def get_start_vertex(self):
        """

        Returns
        -------
        vertex
            a random vertex from this graph

        """
        return min(self.vertices, key=lambda vertex: vertex.value)

    def verify_vertex_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is present in this BaseGraph

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist

        """
        if BaseGraphNode(vertex) not in self.vertices:
            raise VertexDoesNotExistError(f"Vertex: {vertex}: not present in graph")

    def verify_vertex_not_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is not present in this BaseGraph

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex does exist

        """
        if BaseGraphNode(vertex) in self.vertices:
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
            if node == BaseGraphNode(vertex):
                return node
        
        # Unreachable
        return None
    
    def add_vertex(self, vertex):
        """
        
        Parameters
        ----------
        vertex : int, string, etc.
            vertex to insert

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
        self.vertices.add(BaseGraphNode(vertex))
        
        return True

    def remove_vertex(self, vertex):
        """
        
        Parameters
        ----------
        vertex : int, string, etc.
            vertex to remove

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
        self.vertices.discard(BaseGraphNode(vertex))
        
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
        GraphOperationError
            if self is a BaseGraph
        VertexDoesNotExistError
            if the given vertex does not exist (see verify_vertex_present())
                    
        Returns
        -------
        bool
            true on successful add

        """
        if type(self) == BaseGraph:
            raise GraphOperationError("Base Graphs do not support edges")
        
        self.verify_vertex_present(vertex1)
        self.verify_vertex_present(vertex2)

        new_node = self.get_vertex(vertex1)
        self.vertices.discard(new_node)
        
        if not self.directed and vertex1 != vertex2:
            vertex2_node = self.get_vertex(vertex2)
            self.vertices.discard(vertex2_node)

            if weight is not None:
                vertex2_node.insert_neighbor(new_node.value, weight)
            else:
                vertex2_node.insert_neighbor(new_node.value)
            self.vertices.add(vertex2_node)
        
        if weight is not None:
            new_node.insert_neighbor(vertex2, weight)
        else:
            new_node.insert_neighbor(vertex2)
        self.vertices.add(new_node)
        
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
        GraphOperationError
            if self is a BaseGraph
        VertexDoesNotExistError
            if the given vertex does not exist (see verify_vertex_present())

        Returns
        -------
        bool
            True on success

        """
        if type(self) == BaseGraph:
            raise GraphOperationError("Base Graphs do not support edges")
            
        self.verify_vertex_present(vertex1)
        self.verify_vertex_present(vertex2)
        
        new_node = self.get_vertex(vertex1)
        self.vertices.discard(new_node)
        
        if not self.directed and vertex1 != vertex2:
            vertex2_node = self.get_vertex(vertex2)
            self.vertices.discard(vertex2_node)
            if weight is not None:
                vertex2_node.remove_neighbor(new_node.value, weight)
            else:
                vertex2_node.remove_neighbor(new_node.value)
            self.vertices.add(vertex2_node)

        if weight is not None:
            new_node.remove_neighbor(vertex2, weight)
        else:
            new_node.remove_neighbor(vertex2)
        self.vertices.add(new_node)
        
        return True

    def union(self, other):
        """
        
        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the union with

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the union of the Graphs

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph union can only be performed on graphs of same type")
        elif type(self) == BaseGraph:
            self.vertices = self.vertices.union(other.vertices)
        else:
            for vertex in other.vertices:
                if vertex not in self.vertices:
                    new_vertex = vertex
                    if other.multiple_edges != self.multiple_edges:
                        new_vertex = deepcopy(vertex)
                        new_vertex.update_multiple_edges(self.multiple_edges)
                    
                    self.vertices.add(new_vertex)
                else:
                    node = self.get_vertex(vertex.value)
                    self.vertices.discard(node)
                    node += vertex
                    self.vertices.add(node)
        
        return self
    
    def intersection(self, other):
        """
        
        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the intersection with

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the intersection of the Graphs

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph intersection can only be performed on graphs of same type")
        elif type(self) == BaseGraph:
            self.vertices = self.vertices.intersection(other.vertices)
        else:            
            vertices_copy = deepcopy(self.vertices)
            
            for vertex in vertices_copy:
                if vertex not in other.vertices:
                    self.vertices.discard(vertex)
                
            for vertex in self.vertices:
                for node in other.vertices:
                    if vertex == node:
                        vertex.intersection(node)
                        break
        
        return self
    
    def difference(self, other):
        """
        
        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the difference between the Graphs

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
        elif type(self) == BaseGraph:
            self.vertices = self.vertices.difference(other.vertices)
        else:                 
            vertices_copy = deepcopy(self.vertices)
            
            for vertex in vertices_copy:
                if vertex in other.vertices:
                    self.vertices.discard(vertex)
            # remove phantom edges
            for vertex in self.vertices:
                for vertex2 in other.vertices:
                    while vertex.is_neighbor(vertex2.value):
                        vertex.remove_neighbor(vertex2.value)

        return self
    
    def empty(self):
        """
        
        Returns
        -------
        bool
            true if this is an empty graph

        """
        return len(self.vertices) == 0
    
    def name(self):
        """
        
        Returns
        -------
        string
            graph type name

        """
        return "Base Graph"
    
    def join(self, other, default_weight=None):
        """
        
        Parameters
        ----------
        other : 
            the other graph's vertices to join this one's with
        default_weight : int, optional
            the weight to use for joined edges in Weighted Graphs. Leave blank for Unweighted Graphs.

        Raises
        ------
        GraphOperationError
            if other is a BaseGraph

        Returns
        -------
        set of vertices

        """
        if type(self) == BaseGraph:
            raise GraphOperationError("Graph join function not supported for Base Graphs")
            
        vertices_copy = deepcopy(self.vertices)
        other_copy = deepcopy(other.vertices)
        
        for vertex in vertices_copy:
            for node in other_copy:
                if vertex != node:
                    if not vertex.is_neighbor(node.value):
                        if default_weight is not None:
                            vertex.insert_neighbor(node.value, self.default_weight)
                        else:
                            vertex.insert_neighbor(node.value)             
                    if not self.directed and not node.is_neighbor(vertex.value):
                        if default_weight is not None:
                            node.insert_neighbor(vertex.value, self.default_weight)
                        else:
                            node.insert_neighbor(vertex.value)
                else:
                    vertex.union(node)
        
        for vertex in other_copy:
            if vertex not in vertices_copy:
                new_vertex = vertex
                if other.multiple_edges != self.multiple_edges:
                    new_vertex = deepcopy(vertex)
                    new_vertex.update_multiple_edges(self.multiple_edges)
                    
                vertices_copy.add(new_vertex)
        
        return vertices_copy
    
    def __add__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the join (union) with since there are no edges

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the join of the BaseGraphs as a new BaseGraph

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")
            
        graph = BaseGraph()
        graph.vertices = self.vertices.union(other.vertices)
        return graph
    
    def __iadd__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the join (union) with since there are no edges

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the join of the BaseGraphs

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")
            
        return self.union(other)
    
    def __sub__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the difference between the Graphs as a new Graph

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
        elif type(self) == BaseGraph:
            graph = BaseGraph()
            graph.vertices = self.vertices.difference(other.vertices)
            return graph
        else:
            vertices_copy = deepcopy(self.vertices)

            for vertex in self.vertices:
                if vertex in other.vertices:
                    vertices_copy.discard(vertex)
                
            for vertex in vertices_copy:
                for node in other.vertices:
                    if vertex == node:
                        vertex.difference(node)
                        break
            
            return vertices_copy
    
    def __isub__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not a child of BaseGraph

        Returns
        -------
        BaseGraph
            the difference between the Graphs

        """
        if not isinstance(other, BaseGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
            
        return self.difference(other)
    
    def __eq__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, BaseGraph):
            return False
        
        if len(self.vertices) != len(other.vertices):
            return False
        
        for vertex in self.vertices:
            if vertex not in other.vertices:
                return False

        return True
    
    def __ne__(self, other):
        """

        Parameters
        ----------
        other : BaseGraph
            the other BaseGraph to compare

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
            this BaseGraph as a string

        """
        graph_string = self.name() + ":\n"
        for vertex in self.vertices:
            graph_string += vertex.__str__()
        
        if self.empty():
            graph_string = "Empty Base Graph"
        
        return graph_string
