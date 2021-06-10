from typing import List
from core.a_star import AStar
from utils.utils import convertImgToGridData, convertNodesToXYPair, parseArguments
from PIL import Image
from graphics.grid import Grid
import argparse

def main():
    # parse command line arguments
    args: argparse.Namespace = parseArguments()

    # load the image then convert it to readable data
    im = Image.open(args.grid)
    gridData = convertImgToGridData(im)

    if args.windowSize:
        print(f"Drawing a window of {args.windowSize[0]} by {args.windowSize[1]} pixels")

    gridDisplay = Grid(
        width = im.width, 
        height = im.height, 
        gridScaling = args.gridScale if args.gridScale else 7, 
        rows = im.height, 
        columns = im.width, 
        windowWidth = args.windowSize[0] if args.windowSize else 720, 
        windowHeight = args.windowSize[1] if args.windowSize else 720
    )

    # initialize pygame and grid screen 
    gridDisplay.init()
    gridDisplay.setRefreshSpeed(0.06)

    # specify the colors of each elements
    colors = {
        0: (217, 156, 121),
        2: (0, 255, 0),
        3: (0, 0, 255),
        1: (64, 1, 1)
    }

    # apply coloring
    pixelData = [[colors[col] for col in row] for row in gridData['imageData']]

    # set 'pixelData' as color data source for grid display
    gridDisplay.setGridColorData(pixelData)
    gridDisplay.update()

    # run A* path finder
    # 'debugClosedList' will not be empty if 'showExploredArea' is set to True
    solvedPathNodes, debugClosedList = AStar(
        grid = gridData['imageData'], 
        startNode = gridData['startNode'], 
        endNode = gridData['endNode'], 
        showExploredArea = True if args.showExplored else False,

        # setting this to 0 will cause snapshot to happen everytime the algorithm
        # explored a new neighbour node
        exploredAreaSnapshotInterval = args.exploreInterval if args.exploreInterval else 80
    )
    
    solvedPath = convertNodesToXYPair(solvedPathNodes)
    # the resulting path starts from the 'endNode', reverse it to start from 'startNode'
    solvedPath.reverse()

    # visualize the area explored by the algorithm
    for snapshot in debugClosedList:
        for node in snapshot:
            pixelData[node[1]][node[0]] = (242, 242, 242) # color of the explored area
        gridDisplay.update()

    # unlimit screen refresh
    gridDisplay.setRefreshSpeed(0)

    # setting this to a value bigger than 1 will cause the path to be skipped at Nth
    # interval
    pathDrawInterval = args.pathInterval if args.pathInterval else 1
    pathDrawIter = 0

    # visualize the path created by the algorithm
    for point in solvedPath:
        pixelData[point[1]][point[0]] = (166, 73, 65) # color of the path
        pathDrawIter += 1
        if pathDrawIter > pathDrawInterval:
            gridDisplay.update()
            pathDrawIter = 0

    # keep looping forever till user exits the window
    while 1:
        gridDisplay.update()

main()