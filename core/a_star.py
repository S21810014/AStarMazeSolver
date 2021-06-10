from typing import List
from utils.utils import backtrack, calculateDistance, calculateFScore, neighbour
from core.node import Node

def AStar(grid: List[List[int]], startNode: Node, endNode: Node, showExploredArea: bool=False, exploredAreaSnapshotInterval: int=25) -> List[Node]:
    """
    Perform A* path finding to a given Grid

    Parameters
    ----------
    grid : ``List[List[int]]``
        2D array of the grid
    
    startNode : ``Node``
        The starting ``Node`` object
    
    endNode : ``Node``
        The goal ``Node`` object
    
    showExploredArea : ``bool`` [default = ``False``]
        If set to ``True``, will cause the algorithm to keeps
        track of explored area at certain interval and returns
        it as the second output
    
    exploredAreaSnapshotInterval : ``int`` [default = ``25``]
        The interval in which the algorithm will track the
        explored area. Lowest number ``1`` will cause the
        the algorithm to track explored area everytime new
        neighbour is explored.
    """
    openSet = set()
    closedSet = set()

    # used for visualizing explored path
    debugClosedList = []
    debugSnapshotIter = 0

    openSet.add(startNode)

    while len(openSet) > 0:
        # retrieve node with smallest fCost.
        # can be made faster if openSet is a priority queue or a minheap
        current: Node = min(openSet, key=lambda elem: elem.fCost)

        openSet.remove(current)
        closedSet.add(current)

        # we found the goal, return with the path from 'endNode' to the 'startNode'
        if current == endNode:
            return backtrack(startNode, current), debugClosedList

        # explore a new neighbour node in all 4 directions
        for neighbourNode in neighbour(grid, current):
            if neighbourNode in closedSet:
                continue

            newPathGCost = current.gCost + calculateDistance(current, neighbourNode)

            if newPathGCost < neighbourNode.gCost or neighbourNode not in openSet:
                calculateFScore(neighbourNode, endNode)
                
                openSet.add(neighbourNode)
                
                # make a copy of current closedSet elements for visualization purpose
                if showExploredArea:
                    debugSnapshotIter += 1
                    if debugSnapshotIter > exploredAreaSnapshotInterval:
                        tempDebugList = [(x.x, x.y) for x in closedSet]
                        debugClosedList.append(tempDebugList)
                        debugSnapshotIter = 0
    
    return None
