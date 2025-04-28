from util import manhattanDistance

from game import Grid
import os
import random
from functools import reduce

class Layout:
    """
    A Layout manages the static information about game borad
    """

    def __init__(self, layoutText) -> None:
        # Intitalize width and height based on the layoutText dimesions.
        self.width: int = len(layoutText[0])
        self.height: int = len(layoutText)
        # Grid to represent walls, food and agents' position.
        self.walls: Grid = Grid(self.width, self.height, False)
        self.food: Grid = Grid(self.width, self.height, False)
        self.capsules = [] # List to store capsule positions.
        self.agentPositions = [] # List for number of ghosts.
        # Processing layout text to initialize the layout
        self.processLayoutText(layoutText)
