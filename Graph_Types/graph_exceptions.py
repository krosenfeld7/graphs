"""Graph related exceptions for Graphs, Adjacency Lists and Matrices
"""

class NeighborDoesNotExistError(Exception):
    pass


class NeighborAlreadyExistsError(Exception):
    pass


class VertexOperationError(Exception):
    pass


class VertexDoesNotExistError(Exception):
    pass


class VertexAlreadyExistsError(Exception):
    pass


class GraphOperationError(Exception):
    pass


class AdjacencyListOperationError(Exception):
    pass


class AdjacencyMatrixOperationError(Exception):
    pass

class ConversionOperationError(Exception):
    pass
