"""The UnweightedGraphNode class implements a simple unweighted graph node. This class inherits the
   BaseGraphNode class. This Unweighted Graph Node supports multiple edges and common node operations.
"""

from .base_graph_node import BaseGraphNode
from .graph_exceptions import NeighborDoesNotExistError
from .graph_exceptions import NeighborAlreadyExistsError
from .graph_exceptions import VertexOperationError
from copy import deepcopy


class UnweightedGraphNode(BaseGraphNode):
    
    def __init__(self, value, multiple_edges=False):
        super().__init__(value)
        self.multiple_edges = multiple_edges
        self.neighbors = set() if not multiple_edges else {}

    def get_neighbors(self):
        if not self.multiple_edges:
            return list(self.neighbors)

        return list(self.neighbors.keys())

    def insert_neighbor(self, neighbor):
        """
        
        Parameters
        ----------
        neighbor : int, string, etc.
            neighbor to add

        Raises
        ------
        NeighborAlreadyExistsError
            if the given edge already exists

        Returns
        -------
        bool
            true if neighbor was successfully added

        """
        if neighbor not in self.neighbors and not self.multiple_edges:
            self.neighbors.add(neighbor)
            return True
        elif self.multiple_edges:
            if neighbor not in self.neighbors:
                self.neighbors[neighbor] = 1
            else:
                self.neighbors[neighbor] += 1
            return True
        
        raise NeighborAlreadyExistsError(f"Neighbor: {neighbor}: "
                                         f"already present for vertex: {self.value}")
    
    def remove_neighbor(self, neighbor):
        """
        
        Parameters
        ----------
        neighbor : int, string, etc.
            neighbor to remove

        Raises
        ------
        NeighborDoesNotExistError
            if the given edge does not exist

        Returns
        -------
        bool
            if the neighbor was successfully removed

        """
        if neighbor in self.neighbors and not self.multiple_edges:
            self.neighbors.discard(neighbor)
            return True
        elif neighbor in self.neighbors and self.multiple_edges:
            self.neighbors[neighbor] -= 1
            if self.neighbors[neighbor] == 0:
                del self.neighbors[neighbor]
            return True
        
        raise NeighborDoesNotExistError(f"Neighbor: {neighbor}: "
                                        f"not present for vertex: {self.value}")
    
    def is_neighbor(self, neighbor):
        """
        
        Parameters
        ----------
        neighbor : int, string, etc.
            neighbor to check

        Returns
        -------
        bool
            if the given neighbor is a neighbor

        """
        if neighbor in self.neighbors:
            return True
        
        return False
    
    def disconnected(self):
        """
        
        Returns
        -------
        bool
            true if this node has no neighbors

        """
        return len(self.neighbors) == 0
    
    def update_multiple_edges(self, multiple_edges):
        """

        Parameters
        ----------
        multiple_edges : bool
            field to update this node's multiple edge status to

        """
        if not self.multiple_edges and self.multiple_edges != multiple_edges:
            self.neighbors = dict.fromkeys(self.neighbors, 1)            
        elif self.multiple_edges and self.multiple_edges != multiple_edges:
            self.neighbors = set(self.neighbors.keys())
        
        self.multiple_edges = multiple_edges
    
    def union(self, other):
        """
        
        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if the other UnweightedGraphNode is not equal

        Returns
        -------
        UnweightedGraphNode
            the union of the UnweightedGraphNodes

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be added to by vertex: {other.value}")
        
        if not self.multiple_edges and not other.multiple_edges:
            self.neighbors = self.neighbors.union(other.neighbors)
        elif self.multiple_edges and not other.multiple_edges:
            for key in other.neighbors:
                if key in self.neighbors:
                    dict(self.neighbors)[key] += 1
                else:
                    dict(self.neighbors)[key] = 1
        elif not self.multiple_edges and other.multiple_edges:
            for key in other.neighbors:
                if key not in self.neighbors:
                    self.neighbors.add(key)
        else:
            for key in other.neighbors:
                if key in self.neighbors:
                    dict(self.neighbors)[key] += dict(other.neighbors)[key]
                else:
                    dict(self.neighbors)[key] = dict(other.neighbors)[key]
        
        return self
    
    def intersection(self, other):
        """
        
        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the intersection with

        Raises
        ------
        VertexOperationError
            if the other UnweightedGraphNode is not equal

        Returns
        -------
        UnweightedGraphNode
            the intersection of the UnweightedGraphNodes

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be intersected with vertex: {other.value}")
        
        if not self.multiple_edges and not other.multiple_edges:
            self.neighbors = self.neighbors.intersection(other.neighbors)
        else:
            self_dict = deepcopy(self.neighbors)
            if not self.multiple_edges and other.multiple_edges:
                for key in self_dict:
                    if key not in other.neighbors:
                        self.neighbors.discard(key)
            else:
                for key in self_dict:
                    if key not in other.neighbors:
                        del dict(self.neighbors)[key]
                    elif not other.multiple_edges:
                        dict(self.neighbors)[key] = 1
                    else:
                        dict(self.neighbors)[key] = min(dict(self.neighbors)[key],
                                                        dict(other.neighbors)[key])
            
        return self
    
    def difference(self, other):
        """
        
        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other UnweightedGraphNode is not equal

        Returns
        -------
        UnweightedGraphNode
            the difference between this UnweightedGraphNode and other

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be subtracted by vertex: {other.value}")
        
        if not self.multiple_edges and not other.multiple_edges:
            self.neighbors = self.neighbors.difference(other.neighbors)
        else:
            self_dict = deepcopy(self.neighbors)
            if not self.multiple_edges and other.multiple_edges:
                for key in self_dict:
                    if key in other.neighbors:
                        self.neighbors.discard(key)
            else:
                for key in self_dict:
                    if key in other.neighbors:
                        del dict(self.neighbors)[key]
        
        return self
    
    def __add__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if other is not a UnweightedGraphNode

        Returns
        -------
        UnweightedGraphNode
            the union of the UnweightedGraphNodes as a new UnweightedGraphNode

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be added to by vertex: {other.value}")
        
        node = UnweightedGraphNode(self.value, self.multiple_edges)

        if not self.multiple_edges and not other.multiple_edges:
            node.neighbors = self.neighbors.union(other.neighbors)
        else:
            node.neighbors = deepcopy(self.neighbors)
            if self.multiple_edges and not other.multiple_edges:
                for key in other.neighbors:
                    if key in node.neighbors:
                        node.neighbors[key] += 1
                    else:
                        node.neighbors[key] = 1
            elif not self.multiple_edges and other.multiple_edges:
                for key in other.neighbors:
                    if key not in node.neighbors:
                        node.neighbors.add(key)
            else:
                for key in other.neighbors:
                    if key in node.neighbors:
                        node.neighbors[key] += other.neighbors[key]
                    else:
                        node.neighbors[key] = other.neighbors[key]
                    
        return node
    
    def __iadd__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if other is not a UnweightedGraphNode (see union())

        Returns
        -------
        UnweightedGraphNode
            the union of the UnweightedGraphNodes

        """
        return self.union(other)
    
    def __sub__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other UnweightedGraphNode is not equal

        Returns
        -------
        UnweightedGraphNode
            the difference between this UnweightedGraphNode and other as a new UnweightedGraphNode

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be subtracted by vertex: {other.value}")
        
        node = UnweightedGraphNode(self.value, self.multiple_edges)
        
        if not self.multiple_edges and not other.multiple_edges:
            node.neighbors = self.neighbors.difference(other.neighbors)
        else:
            node.neighbors = deepcopy(self.neighbors)
            if not self.multiple_edges and other.multiple_edges:
                for key in self.neighbors:
                    if key in other.neighbors:
                        node.neighbors.discard(key)
            else:
                for key in self.neighbors:
                    if key in other.neighbors:
                        del node.neighbors[key]
                        
        return node
    
    def __isub__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other UnweightedGraphNode is not equal (see difference())

        Returns
        -------
        UnweightedGraphNode
            the difference between this UnweightedGraphNode and other

        """
        return self.difference(other)
        
    def __eq__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, UnweightedGraphNode):
            return False

        if self.value != other.value:
            return False
        
        return True
    
    def __ne__(self, other):
        """

        Parameters
        ----------
        other : UnweightedGraphNode
            the other UnweightedGraphNode to compare

        Returns
        -------
        bool
            true if other is not equal to self

        """
        return not self == other
    
    def __hash__(self):
        """

        Returns
        -------
        hash
            hash for this UnweightedGraphNode object used for comparison

        """
        return BaseGraphNode.__hash__(self)
    
    def __str__(self):
        """

        Returns
        -------
        string
            this UnweightedGraphNode as a string

        """
        if self.disconnected():
            return f"{self.value}: No neighbors\n"
        
        return f"{self.value}: {self.neighbors}\n"
    
