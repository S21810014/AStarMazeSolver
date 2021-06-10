class Node:
    """
    A Class describing a Node.


    Attributes
    ----------
    parent : ``Node``
        a reference to a parent Node object
    x : ``int``
        the x coordinate of the node
    y : ``int``
        the y coordinate of the node
    fCost : ``float``
        the total cost of the node, f(n) = g(n) + h(n)
    gCost : ``float``
        the distance between current node and the starting node
    """

    def __init__(self, parent, x, y, fCost, gCost):
        self.parent = parent
        self.x = x
        self.y = y
        self.fCost = fCost
        self.gCost = gCost

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        
        return False
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(str(self))
