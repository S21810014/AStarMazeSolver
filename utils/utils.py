from typing import List, TypedDict
from PIL.Image import Image
from core.node import Node
import math
import argparse

class GridData(TypedDict):
    """
    Key
    ---
    imageData : ``List[List[int]]``
        2D array of the grid
    startNode : ``Node``
        Node object representing
        starting Node
    endNode : ``Node``
        Node object representing
        goal Node
    """
    imageData: List[List[int]]
    startNode: Node
    endNode: Node


def convertImgToGridData(image: Image) -> GridData:
    """
    Converts RGB bitmap data to GridData containing
    integer-coded 2D array of the grid, a startNode,
    and an endNode
    
    
    Parameter
    ----------
    image : ``Image``
        RGB Image data

    Returns
    -------
    ``GridData``
        A Dictionary consisting of ``imageData``,
        ``startNode``, and ``endNode`` key
    """
    startNode = None
    endNode = None
    imgData = []

    for row in range(image.height):
        temp = []

        for col in range(image.width):
            pixel = image.getpixel((col, row))

            # treat pixel as wall if red channel value is over 127
            if pixel[0] > 127:
                temp.append(0)
            
            # treat pixel as finish node if green channel value is over 127
            elif pixel[1] > 127:
                endNode = Node(None, col, row, 0, 0)
                temp.append(2)

            # treat pixel as start node if blue channel value is over 127
            elif pixel[2] > 127:
                startNode = Node(None, col, row, 0, 0)
                temp.append(3)

            # treat as empty, walkable space if all channel values are less than 127
            else:
                temp.append(1)
        
        imgData.append(temp)
    
    return {'imageData': imgData, 'startNode': startNode, 'endNode': endNode}

def convertNodesToXYPair(nodes: List[Node]) -> List[int]:
    """
    Convert a ``list`` of ``Node`` objects to a 
    ``list`` of ``(x, y)`` pair

    Parameter
    ----------
    nodes : ``List[Node]``
        ``list`` of ``Node`` objects

    Returns
    -------
    ``List[int]``
        ``list`` of ``(x, y)`` pair
    """
    xyPair = []

    for node in nodes:
        xyPair.append((node.x, node.y))
    
    return xyPair
    
def calculateDistance(firstNode: Node, secondNode: Node) -> float:
    """
    Calculates the distance between two ``Node`` objects

    Parameters
    ----------
    firstNode : ``Node``
        The starting ``Node``
    secondNode : ``Node``
        The target ``Node``
    
    Returns
    -------
    ``float``
        The distance between the two ``Node``s
    """
    # Euclidean
    # commented. Too slow for non-diagonal path
    # return math.sqrt(math.pow(firstNode.x-secondNode.x, 2) + math.pow(firstNode.y-secondNode.y, 2))

    # Manhattan
    return abs(firstNode.x - secondNode.x) + abs(firstNode.y - secondNode.y)

def calculateFScore(node: Node, endNode: Node):
    """
    Calculates the fCost of a given ``Node`` object

    Parameters
    ----------
    node : ``Node``
        The ``Node`` which fCost will be calculated
    endNode : ``Node``
        The ``Node`` to be used for calculating hCost
    
    **INPLACE**
    """
    node.fCost = node.gCost + calculateDistance(node, endNode)

def neighbour(grid: List[List[int]], node: Node) -> List[Node]:
    """
    Generates a new neighbour ``Node``s from the current ``Node``

    Parameters
    ----------
    grid : ``List[List[int]]``
        2D array of the grid. Used to determine if the ``Node``s
        new location is out of bound or on a wall
    node : ``Node``
        Target ``Node`` where new neighbour will be generated
        from
    
    Returns
    -------
    ``List[Node]``
        ``list`` of new ``Node``s which is the neighbour of
        the target ``Node``
    """
    neighbourNodes = []

    positions = [
        {'x': node.x - 1, 'y': node.y}, # left
        {'x': node.x + 1, 'y': node.y}, # right
        {'x': node.x, 'y': node.y - 1}, # up
        {'x': node.x, 'y': node.y + 1}  # down
    ]

    for position in positions:
        # current position is out of bound from the grid
        if position['y'] >= len(grid) or position['x'] >= len(grid[position['y']]):
            continue

        if grid[position['y']][position['x']] != 1:
            newNode = Node(node, position['x'], position['y'], 0, 0)
            newNode.gCost = node.gCost + calculateDistance(node, newNode)
            neighbourNodes.append(newNode)
    
    return neighbourNodes

def backtrack(startNode: Node, endNode: Node) -> List[Node]:
    """
    Perform a backtrack upon the target ``Node`` by keeping track
    of the parents of the target ``Node`` until it reaches the
    ending ``Node``

    Parameters
    ----------
    startNode : ``Node``
        The target ``Node`` to start from
    endNode : ``Node``
        The ending ``Node`` to end to

    Returns
    -------
    ``List[Node]``
        ``list`` containing the path of ``Node``s between startNode
        and endNode
    """
    nodePath = []

    currentNode = endNode
    while currentNode != startNode:
        nodePath.append(currentNode)
        currentNode = currentNode.parent
    
    return nodePath

def parseArguments() -> argparse.Namespace:
    """
    Parses the argument given by user from commandline

    Returns
    -------
    ``argparse.Namespace``
        the ``Namespace`` object to access the arguments
    """
    parser = argparse.ArgumentParser()

    arguments = [
        ['grid', 'Bitmap File to be solved'],
        ['--windowSize', 'Size of the window'],
        ['--showExplored', 'Render explored area', True],
        ['--gridScale', 'Scale of each cells within the grid'],
        ['--exploreInterval', 'How frequent should the algorithm tracks the explored area'],
        ['--pathInterval', 'How many frames to skip when displaying the solved path']
    ]

    for argument in arguments:
        if len(argument) > 2:
            parser.add_argument(argument[0], help=argument[1], nargs='?', const=argument[2])
        else:
            parser.add_argument(argument[0], help=argument[1])
    
    args: argparse.Namespace = parser.parse_args()

    if args.windowSize:
        try:
            windowSize: List[int] = [int(elem) for elem in args.windowSize.split('x')]
            if len(windowSize) < 2:
                raise AssertionError()
            args.windowSize = windowSize
        except ValueError:
            print("Error: invalid windowSize argument")
            return
        except AssertionError:
            print("Error: please specify width and height of the window, eg: 1280x720")
            return
    
    if args.gridScale:
        try:
            gridScale: int = int(args.gridScale)
            args.gridScale = gridScale
        except ValueError:
            print("Error: invalid gridScale argument")
            return
    
    if args.exploreInterval:
        try:
            exploreInterval: int = int(args.exploreInterval)
            args.exploreInterval = exploreInterval
        except ValueError:
            print("Error: invalid exploreInterval argument")
            return
    
    if args.pathInterval:
        try:
            pathInterval: int = int(args.pathInterval)
            args.pathInterval = pathInterval
        except ValueError:
            print("Error: invalid pathInterval argument")
            return
    
    return args