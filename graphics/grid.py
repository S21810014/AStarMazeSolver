import sys, pygame
from typing import List
import time

class Grid:
    """
    A Class that represents the Grid to be displayed

    Attributes
    ----------
    width : ``int``
        width of the grid cell
    height : ``int``
        height of the grid cell
    rows : ``int``
        number of rows the grid have
    columns: ``int``
        number of columns the grid have
    windowWidth: ``int``
        width of the window containing the grid
    windowHeight : ``int``
        height of the window containing the grid

    Methods
    -------
    init()
        initialize pygame and the Grid display
    
    setGridColorData(gridColorData: ``List[List[int]]``)
        set the internal gridColorData attribute to
        point to the specified ``gridColorData`` parameter
    
    setRefreshSpeed(speed: ``float``)
        set the display refresh speed

    update()
        refresh the Grid display
    """
    def __init__(self, width, height, gridScaling, rows, columns, windowWidth, windowHeight) -> None:
        self.width = width * gridScaling
        self.height = height * gridScaling
        self.rows = rows
        self.columns = columns

        self.rectHeight = int(self.height / self.rows)
        self.rectWidth = int(self.width / self.columns)
        self.rectStartX = int(windowWidth/2 - (self.width/2))
        self.rectStartY = int(windowHeight/2 - (self.height/2))
        self.rectEndX = int(windowWidth/2 + (self.width/2))
        self.rectEndY = int(windowHeight/2 + (self.height/2))

        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.screen = None
        self.refreshSpeed = 0

        self.gridColorData = []
    
    def init(self):
        """
        Initialize pygame and the Grid display
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.screen.fill((0, 0, 0))
    
    def setGridColorData(self, gridColorData: List[List[int]]):
        """
        Set the internal gridColorData attribute to
        point to the specified ``gridColorData`` parameter

        Parameter
        ---------
        gridColorData : ``List[List[int]]``
            2D color data of the grid
        """
        self.gridColorData = gridColorData
    
    def setRefreshSpeed(self, speed: float):
        """
        set the display refresh speed
        
        Parameter
        ---------
        speed: ``float``
            The smaller the number, the faster it refresh
        """
        self.refreshSpeed = speed
    
    def update(self):
        """
        refresh the Grid display
        """
        self.screen.fill((242, 242, 242))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # draws the grid
        for row, colorRow, in zip(range(self.rectStartY, self.rectEndY, self.rectHeight), self.gridColorData):
            for col, color, in zip(range(self.rectStartX, self.rectEndX, self.rectWidth), colorRow):
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    pygame.Rect(col, row, self.rectWidth, self.rectHeight)
                )
        
        # draws a 1 pixel width border around the grid, modify the 'width' parameter to make it thicker
        pygame.draw.rect(
            self.screen, 
            (255, 255, 255), 
            pygame.Rect(
                self.windowWidth/2 - (self.width/2), 
                self.windowHeight/2 - (self.height/2), 
                self.width, 
                self.height
            ), width=1
        )

        # flip the shown buffer to this newly drawn frame
        pygame.display.flip()
        time.sleep(self.refreshSpeed)
