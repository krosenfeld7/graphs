"""The BaseGraphNode class implements a simple graph node. This class is intended to be
   derived and not used directly.
"""

class BaseGraphNode:
    
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        """

        Parameters
        ----------
        other : BaseGraphNode
            the other Graph Node to compare

        Returns
        -------
        bool
            true if other is equal to self

        """
        if not isinstance(other, BaseGraphNode):
            return False
        
        if self.value != other.value:
            return False
        
        return True
    
    def __ne__(self, other):
        """

        Parameters
        ----------
        other : BaseGraphNode
            the other Graph Node to compare

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
            hash for this Graph Node object used for comparison

        """
        return hash(self.value)
    
    def __str__(self):
        """

        Returns
        -------
        string
            this Graph Node as a string

        """
        return f"{self.value}: No neighbors\n"
