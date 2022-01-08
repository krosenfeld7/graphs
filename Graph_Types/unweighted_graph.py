"""The UnweightedGraph class implements a simple unweighted graph. This class inherits the BaseGraph
   class. This Unweighted Graph supports multiple edges between each vertex and can be directed
   or undirected. This graph supports common graph operations such as union, intersection, difference
   and join.
"""

from .base_graph import BaseGraph
from .unweighted_graph_node import UnweightedGraphNode
from .graph_exceptions import *


class UnweightedGraph(BaseGraph):
    
    def __init__(self, directed=True, multiple_edges=False):
        super().__init__()
        self.vertices = set()
        self.directed = directed
        self.multiple_edges = multiple_edges

    def verify_vertex_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is present in this UnweightedGraph

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist

        """
        if UnweightedGraphNode(vertex) not in self.vertices:
            raise VertexDoesNotExistError(f"Vertex: {vertex}: not present in graph")

    def verify_vertex_not_present(self, vertex):
        """

        Parameters
        ----------
        vertex : int, string, etc.
            vertex to verify is not present in this UnweightedGraph

        Raises
        ------
        VertexAlreadyExistsError
            if the given vertex does exist

        """
        if UnweightedGraphNode(vertex) in self.vertices:
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
            if node == UnweightedGraphNode(vertex):
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
        self.vertices.add(UnweightedGraphNode(vertex, self.multiple_edges))
        
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
        self.vertices.discard(UnweightedGraphNode(vertex))

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
            will always be set to None for UnweightedGraphs

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see BaseGraph.add_edge())
            
        Returns
        -------
        bool
            if the new edge was added successfully

        """
        return super().add_edge(vertex1, vertex2)
        
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
            will always be set to None for UnweightedGraphs

        Raises
        ------
        VertexDoesNotExistError
            if the given vertex does not exist (see BaseGraph.remove_edge())

        Returns
        -------
        bool
            if the edge was removed successfully
        
        """
        return super().remove_edge(vertex1, vertex2)
    
    def union(self, other):
        """
        See BaseGraph.union() for more details

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the union with

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the union of the Graphs

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph union can only be performed on graphs of same type")

        return super().union(other)
    
    def intersection(self, other):
        """
        See BaseGraph.intersection() for more details
        
        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the intersection with

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the intersection of the UnweightedGraphs

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph intersection can only be performed on graphs of same type")
        
        return super().intersection(other)
    
    def difference(self, other):
        """
        See BaseGraph.difference() for more details

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the difference between the UnweightedGraphs

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
               
        return super().difference(other)
    
    def set_directed(self, directed):
        """

        Parameters
        ----------
        directed : bool
            field indicating if UnweightedGraph will be updated to directed or not

        """
        self.directed = directed
    
    def name(self):
        """
        
        Returns
        -------
        string
            UnweightedGraph string name

        """
        name_string = "Unweighted "
        name_string += "Directed " if self.directed else "Undirected "
        name_string += "Multi-graph" if self.multiple_edges else "Graph"
        
        return name_string
    
    def __add__(self, other):
        """
        See BaseGraph.join() for more details

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the join with

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the join of the UnweightedGraphs as a new UnweightedGraph

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")
                
        graph = UnweightedGraph()
        graph.vertices = super().join(other)
        graph.directed = self.directed
        graph.multiple_edges = self.multiple_edges
        
        return graph
    
    def __iadd__(self, other):
        """
        See BaseGraph.join() for more details

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the join with

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the join of the UnweightedGraphs

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph join can only be performed on graphs of same type")
            
        self.vertices = super().join(other)
        return self
    
    def __sub__(self, other):
        """
        See BaseGraph.__sub__() for more details

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the difference between the UnweightedGraphs as a new UnweightedGraph

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
            
        graph = UnweightedGraph()
        graph.vertices = super().__sub__(other)
        graph.directed = self.directed
        graph.multiple_edges = self.multiple_edges
        return graph
    
    def __isub__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to find the difference with this one

        Raises
        ------
        GraphOperationError
            if other is not an UnweightedGraph

        Returns
        -------
        UnweightedGraph
            the difference between the UnweightedGraphs

        """
        if not isinstance(other, UnweightedGraph):
            raise GraphOperationError("Graph difference can only be performed on graphs of same type")
            
        return self.difference(other)
    
    def __eq__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraph
            the other UnweightedGraph to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, UnweightedGraph):
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
        other : UnweightedGraph
            the other UnweightedGraph to compare

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
            this UnweightedGraph as a string

        """
        graph_string = self.name() + ":\n"
        for vertex in sorted(self.vertices, key=lambda x: x.value):
            graph_string += vertex.__str__()
        
        if self.empty():
            graph_string = "Empty Graph\n"
        
        return graph_string
