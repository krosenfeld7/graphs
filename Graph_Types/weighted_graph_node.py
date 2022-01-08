"""The WeightedGraphNode class implements a simple unweighted graph node. This class inherits the
   BaseGraphNode class. This Weighted Graph Node supports multiple edges and common node operations.
"""

from collections import Counter
from .base_graph_node import BaseGraphNode
from .graph_exceptions import NeighborDoesNotExistError
from .graph_exceptions import NeighborAlreadyExistsError
from .graph_exceptions import VertexOperationError


class WeightedGraphNode(BaseGraphNode):
    
    def __init__(self, value, multiple_edges=False):
        super().__init__(value)
        self.multiple_edges = multiple_edges
        self.neighbors = {}

    def get_neighbors(self):
        return [[neighbor, self.neighbors[neighbor]] for neighbor in self.neighbors]

    def insert_neighbor(self, neighbor, weight):
        """
        
        Parameters
        ----------
        neighbor : int, string, etc.
            neighbor to add
        weight : int
            weight of the edge between this node and the neighbor

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
            self.neighbors[neighbor] = weight
            return True
        elif self.multiple_edges:
            if neighbor not in self.neighbors:
                self.neighbors[neighbor] = [weight]
            else:
                temp_list = self.neighbors[neighbor]
                temp_list.append(weight)
                self.neighbors[neighbor] = temp_list
            return True
        
        raise NeighborAlreadyExistsError(f"Neighbor: {neighbor}: "
                                         f"already present for vertex: {self.value}")
    
    def remove_neighbor(self, neighbor, weight=None):
        """
        
        Parameters
        ----------
        neighbor : int, string, etc.
            neighbor to remove
        weight : int
            the weight of the edge to remove

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
            del self.neighbors[neighbor]
            return True
        elif neighbor in self.neighbors and self.multiple_edges:
            temp_list = self.neighbors[neighbor]
            if not weight or weight not in temp_list:
                weight = max(temp_list)
            for i in range(len(temp_list)):
                if temp_list[i] == weight:
                    del temp_list[i]
                    break
            
            if len(temp_list) > 0:
                self.neighbors[neighbor] = temp_list
            else:
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
            for key in self.neighbors:
                self.neighbors[key] = [self.neighbors[key]]
                
        elif self.multiple_edges and self.multiple_edges != multiple_edges:
            for key in self.neighbors:
                self.neighbors[key] = min(self.neighbors[key])
        
        self.multiple_edges = multiple_edges    
    
    def union(self, other):
        """
        
        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if the other WeightedGraphNode is not equal

        Returns
        -------
        WeightedGraphNode
            the union of the WeightedGraphNodes

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be added to by vertex: {other.value}")
        
        if not self.multiple_edges:
            for key in self.neighbors:
                if key in other.neighbors:
                    if not other.multiple_edges:
                        self.neighbors[key] = min(self.neighbors[key],
                                                  other.neighbors[key])
                    else:
                        self.neighbors[key] = min(self.neighbors[key],
                                                  min(other.neighbors[key]))
                                    
            for key in other.neighbors:
                if key not in self.neighbors:
                    if not other.multiple_edges:
                        self.neighbors[key] = other.neighbors[key]
                    else:
                        self.neighbors[key] = min(other.neighbors[key])
        
        else:
            for key in self.neighbors:
                if key in other.neighbors:
                    temp_list = self.neighbors[key]
                    if not other.multiple_edges:
                        temp_list.append(other.neighbors[key])
                    else:
                        temp_list.extend(other.neighbors[key])
                    self.neighbors[key] = temp_list
            
            for key in other.neighbors:
                if key not in self.neighbors:
                    temp_list = []
                    if not other.multiple_edges:
                        temp_list.append(other.neighbors[key])
                    else:
                        temp_list.extend(other.neighbors[key])
                    self.neighbors[key] = temp_list
                
        return self
    
    def intersection(self, other):
        """
        
        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the intersection with

        Raises
        ------
        VertexOperationError
            if the other WeightedGraphNode is not equal

        Returns
        -------
        WeightedGraphNode
            the intersection of the WeightedGraphNodes

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be intersected with vertex: {other.value}")
        
        new_neighbors = {}
        
        if not self.multiple_edges and not other.multiple_edges:
            for key in other.neighbors:
                if key in self.neighbors and self.neighbors[key] == other.neighbors[key]:
                    new_neighbors[key] = self.neighbors[key]
                    
        elif not self.multiple_edges and other.multiple_edges:
            for key in other.neighbors:
                if key in self.neighbors and self.neighbors[key] in other.neighbors[key]:
                    new_neighbors[key] = self.neighbors[key]
                    
        elif self.multiple_edges and not other.multiple_edges:
            for key in other.neighbors:
                if key in self.neighbors and other.neighbors[key] in self.neighbors[key]:
                    new_neighbors[key] = [other.neighbors[key]]
                    
        else:
            for key in other.neighbors:
                if key in self.neighbors:
                    temp_list = list((Counter(self.neighbors[key]) &
                                      Counter(other.neighbors[key])).elements())
                    if len(temp_list) > 0:
                        new_neighbors[key] = temp_list

        self.neighbors = new_neighbors
        
        return self
    
    def difference(self, other):
        """
        
        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other WeightedGraphNode is not equal

        Returns
        -------
        WeightedGraphNode
            the difference between this WeightedGraphNode and other

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be subtracted by vertex: {other.value}")
        
        new_neighbors = {}
        if not self.multiple_edges and not other.multiple_edges:
            for key in self.neighbors:
                if key not in other.neighbors or other.neighbors[key] != self.neighbors[key]:
                    new_neighbors[key] = self.neighbors[key]
                    
        elif not self.multiple_edges and other.multiple_edges:
            for key in self.neighbors:
                if key not in other.neighbors or self.neighbors[key] not in other.neighbors[key]:
                    new_neighbors[key] = self.neighbors[key]
                    
        elif self.multiple_edges and not other.multiple_edges:
            for key in self.neighbors:
                temp_list = self.neighbors[key]
                if key in other.neighbors and other.neighbors[key] in self.neighbors[key]:
                    temp_list.remove(other.neighbors[key])
                
                if len(temp_list) > 0:
                    new_neighbors[key] = temp_list
        else:
            for key in self.neighbors:
                temp_list = self.neighbors[key]
                if key in other.neighbors:
                    temp_list = list((Counter(self.neighbors[key]) - Counter(other.neighbors[key])).elements())
                
                if len(temp_list) > 0:
                    new_neighbors[key] = temp_list
        
        self.neighbors = new_neighbors
        
        return self
    
    def __add__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if other is not a WeightedGraphNode

        Returns
        -------
        WeightedGraphNode
            the union of the WeightedGraphNodes as a new WeightedGraphNode

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be added to by vertex: {other.value}")
        
        node = WeightedGraphNode(self.value, self.multiple_edges)
        
        if not self.multiple_edges:
            for key in self.neighbors:
                if key in other.neighbors:
                    if not other.multiple_edges:
                        node.neighbors[key] = min(self.neighbors[key], other.neighbors[key])
                    else:
                        node.neighbors[key] = min(self.neighbors[key], min(other.neighbors[key]))
                else:
                    node.neighbors[key] = self.neighbors[key]
            
            for key in other.neighbors:
                if key not in self.neighbors:
                    if not other.multiple_edges:
                        node.neighbors[key] = other.neighbors[key]
                    else:
                        node.neighbors[key] = min(other.neighbors[key])
        else:
            for key in self.neighbors:
                if key in other.neighbors:
                    temp_list = self.neighbors[key]
                    if not other.multiple_edges:
                        temp_list.append(other.neighbors[key])
                    else:
                        temp_list.extend(other.neighbors[key])
                    node.neighbors[key] = temp_list
                else:
                    node.neighbors[key] = self.neighbors[key]
            
            for key in other.neighbors:
                if key not in self.neighbors:
                    temp_list = []
                    if not other.multiple_edges:
                        temp_list.append(other.neighbors[key])
                    else:
                        temp_list.extend(other.neighbors[key])
                    node.neighbors[key] = temp_list
        
        return node
    
    def __iadd__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the union with

        Raises
        ------
        VertexOperationError
            if other is not a WeightedGraphNode (see union())

        Returns
        -------
        WeightedGraphNode
            the union of the WeightedGraphNodes

        """
        return self.union(other)
    
    def __sub__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other WeightedGraphNode is not equal

        Returns
        -------
        WeightedGraphNode
            the difference between this WeightedGraphNode and other as a new WeightedGraphNode

        """
        if self != other:
            raise VertexOperationError(f"Vertex: {self.value} "
                                       f"cannot be subtracted by vertex: {other.value}")
        
        node = WeightedGraphNode(self.value, self.multiple_edges)
        
        if not self.multiple_edges and not other.multiple_edges:
            for key in self.neighbors:
                if key not in other.neighbors or other.neighbors[key] != self.neighbors[key]:
                    node.neighbors[key] = self.neighbors[key]
                    
        elif not self.multiple_edges and other.multiple_edges:
            for key in self.neighbors:
                if key not in other.neighbors or self.neighbors[key] not in other.neighbors[key]:
                    node.neighbors[key] = self.neighbors[key]
                    
        elif self.multiple_edges and not other.multiple_edges:
            for key in self.neighbors:
                temp_list = self.neighbors[key]
                if key in other.neighbors and other.neighbors[key] in self.neighbors[key]:
                    temp_list.remove(other.neighbors[key])
                
                if len(temp_list) > 0:
                    node.neighbors[key] = temp_list
        else:
            for key in self.neighbors:
                temp_list = self.neighbors[key]
                if key in other.neighbors:
                    temp_list = list((Counter(self.neighbors[key]) -
                                      Counter(other.neighbors[key])).elements())
                
                if len(temp_list) > 0:
                    node.neighbors[key] = temp_list
                    
        return node
    
    def __isub__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to find the difference with this one

        Raises
        ------
        VertexOperationError
            if the other WeightedGraphNode is not equal (see difference())

        Returns
        -------
        WeightedGraphNode
            the difference between this WeightedGraphNode and other

        """
        return self.difference(other)
        
    def __eq__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, WeightedGraphNode):
            return False

        if self.value != other.value:
            return False
        
        return True
    
    def __ne__(self, other):
        """

        Parameters
        ----------
        other : WeightedGraphNode
            the other WeightedGraphNode to compare

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
            hash for this WeightedGraphNode object used for comparison

        """
        return BaseGraphNode.__hash__(self)
    
    def __str__(self):
        """

        Returns
        -------
        string
            this WeightedGraphNode as a string

        """
        if self.disconnected():
            return f"{self.value}: No neighbors\n"
        
        return f"{self.value}: {self.neighbors}\n"
    
