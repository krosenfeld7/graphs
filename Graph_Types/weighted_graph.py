"""The WeightedGraph class implements a simple weighted graph. This class inherits the BaseGraph
   class. This Weighted Graph supports multiple edges between each vertex and can be directed
   or undirected. This graph supports common graph operations such as union, intersection, difference
   and join.
"""

from .base_graph import BaseGraph
from .weighted_graph_node import WeightedGraphNode
from .graph_exceptions import *


class WeightedGraph(BaseGraph):
    
    def __init__(self, directed=True, multiple_edges=False, default_weight=0):
        super().__init__()
        self.vertices = set()
        self.directed = directed
        self.default_weight = default_weight
        self.multiple_edges = multiple_edges
        
    def verify_vertex_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is present in this WeightedGraph

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist

        """
        if WeightedGraphNode(vertex) not in self.vertices:
            raise VertexDoesNotExistError(f"Vertex: {vertex}: not present in graph")

    def verify_vertex_not_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is not present in this WeightedGraph

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex does exist

        """
        if WeightedGraphNode(vertex) in self.vertices:
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
            if node == WeightedGraphNode(vertex):
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
        self.vertices.add(WeightedGraphNode(vertex, self.multiple_edges))
        
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
        self.vertices.discard(WeightedGraphNode(vertex))

        for key in self.vertices:
            while key.is_neighbor(vertex):
                key.remove_neighbor(vertex)
        
        return True

    def add_edge(self, vertex1, vertex2, weight=None):
        """
        See BaseGraph.add_edge() for more details
        
        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to add
        vertex2 : int, string, etc.
            target of edge to add
        weight : int
            weight of the edge to add

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see BaseGraph.add_edge())

        Returns
        -------
        bool
            if the new edge was added successfully

        """
        if weight is None:
            weight = self.default_weight
        
        return super().add_edge(vertex1, vertex2, weight)

    def remove_edge(self, vertex1, vertex2, weight=None):
        """
        See BaseGraph.remove_edge() for more details
        
        Parameters
        ----------
        vertex1 : int, string, etc.
            source of edge to remove
        vertex2 : int, string, etc.
            target of edge to remove
        weight : int
            the weight of the edge to remove

        Returns
        -------
        bool
            if the edge was removed successfully
        
        """
        return super().remove_edge(vertex1, vertex2, weight)
    
    def union(self, other):
        """
        See BaseGraph.union() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the union with

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the union of the Graphs

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph union can only be performed on graphs of same type")

        return super().union(other)
    
    def intersection(self, other):
        """
        See BaseGraph.intersection() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the intersection with

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the intersection of the WeightedGraphs

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph intersection can only be performed on graphs of same type")
          
        return super().intersection(other)
    
    def difference(self, other):
        """
        See BaseGraph.difference() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the difference between the WeightedGraphs

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
           
        return super().difference(other)
    
    def set_directed(self, directed):
        """

        Parameters
        ----------
        directed : bool
            field indicating if WeightedGraph will be updated to directed or not

        """
        self.directed = directed
    
    def name(self):
        """
        
        Returns
        -------
        string
            WeightedGraph string name

        """
        name_string = "Weighted "
        name_string += "Directed " if self.directed else "Undirected "
        name_string += "Multi-graph" if self.multiple_edges else "Graph"
        
        return name_string
    
    def __add__(self, other):
        """
        See BaseGraph.join() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the join with

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the join of the WeightedGraphs as a new WeightedGraph

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")
                
        graph = WeightedGraph()
        graph.vertices = super().join(other, self.default_weight)
        graph.directed = self.directed
        graph.default_weight = self.default_weight
        graph.multiple_edges = self.multiple_edges
        
        return graph
    
    def __iadd__(self, other):
        """
        See BaseGraph.join() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the join with

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the join of the WeightedGraphs

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")

        self.vertices = super().join(other, self.default_weight)
        return self

    def __sub__(self, other):
        """
        See BaseGraph.__sub__() for more details

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the difference between the WeightedGraphs as a new WeightedGraph

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
           
        graph = WeightedGraph()
        graph.vertices = super().__sub__(other)
        graph.directed = self.directed
        graph.default_weight = self.default_weight
        graph.multiple_edges = self.multiple_edges
        return graph
    
    def __isub__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an WeightedGraph

        Returns
        -------
        WeightedGraph
            the difference between the WeightedGraphs

        """
        if not isinstance(other, WeightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
           
        return self.difference(other)
    
    def __eq__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraph
            the other WeightedGraph to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, WeightedGraph):
            return False
        
        if self.directed != other.directed:
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
        other : WeightedGraph
            the other WeightedGraph to compare

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
            this WeightedGraph as a string

        """
        graph_string = self.name() + ":\n"
        for vertex in sorted(self.vertices, key=lambda x: x.value):
            graph_string += vertex.__str__()
        
        if self.empty():
            graph_string = "Empty Graph\n"
        
        return graph_string
