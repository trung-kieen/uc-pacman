from typing import List, NamedTuple, NoReturn, Self, Tuple
# from util import *
import time
import os
import traceback
import sys
# class Point(NamedTuple):
#     x: int
#     y: int

Point = Tuple[int, int]

class Agent:
    def __init__(self, index = 0):
        self.index = index


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: NORTH,
            EAST : WEST,
            WEST: EAST,
            STOP: STOP
            }

class Configuration:
    """
    Hold the (x, y) position of agent and it traveling direction
    Not hard code save in AgenState because we need to quick change position
    """

    def __init__ (self, pos, direction):
        self.pos:Point =  pos
        self.direction:Directions = direction

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

    def isInteger(self):
        x, y = self.pos
        return x == int(x) and y == int(y)


    def __eq___(self, other):
        if other == None:
            return False


    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)
    def generateSuccessor(self, vector):
        """
        Generate new configuration base on current configuration and vector
        Action are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector

        # TODO:
        direction = Actions.vectorToDirection(vector)
        if direction == Directions.STOP:
            direction = self.direction
        return Configuration((x + dx , y + dy), direction)


class Actions:
    """
    Collection of static method to manipulate move action
    """


    _directions =  {
            Directions.WEST: (-1, 0),
            Directions.STOP: (0, 0),
            Directions.EAST: (1, 0),
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1),
    }
    _directionsAsList = [
            (Directions.WEST, (-1, 0)),
            (Directions.STOP, (0, 0)),
            (Directions.EAST, (1, 0)),
            (Directions.NORTH, (0, 1)),
            (Directions.SOUTH, (0, -1)),
    ]
    TOLERANCE = 0.001

    @staticmethod
    def directionToVector(direction, speed = 1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)


    @staticmethod
    def vectorToDirection(vector: Point):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST


    @staticmethod
    # TODO: strict type for walls
    def getPossibleActions(config: Configuration, walls):
        possible = []
        x, y = config.pos
        # TODO: explain why
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)) > Actions.TOLERANCE:
            return [config.getDirection()]
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)
        return possible



    @staticmethod
    def reverseDirection(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST



class AgentState:
    """
    Store agent details about configuration, speed, scared status, etc
    """
    def __init__(self, startConfiguration, isPacman):
        self.start: Configuration | None = startConfiguration
        self.configuration: Configuration | None = startConfiguration
        self.isPacman = isPacman
        self.scaredTimer = 0
        # Use for contest only
        self.numCarrying = 0
        self.numReturned = 0
    def __str__(self):
        if self.isPacman:
            return "Pacman: " + str(self.configuration)
        else:
            return "Ghost: " + str(self.configuration)

    def __eq__(self, other: object, /) -> bool:
        if other == None :
            return False
        if not isinstance(other, AgentState):
            return False
        return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

    def __hash__(self) -> int:
        return hash(hash(self.configuration) + 13 * hash(self.scaredTimer))


    def copy(self):
        state = AgentState(self.start, self.isPacman)
        state.configuration = self.configuration
        state.scaredTimer = self.scaredTimer
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        return state
    def getPosition(self) -> None | Point:
        if self.configuration == None:
            return None
        return self.configuration.getPosition()

class Grid:
    """
    A 2-d arrya object composition list of list as grid[x][y]
    with x, y is Point. Starting point of pac man is (0, 0)
    """

    def __init__(self, width: int, height: int, initialValue = False, bitRepesentation = None) -> None:
        if initialValue not in [False, True]:
            raise Exception("Grids con only contain booleans")

        self.CELLS_PER_INT = 30
        self.width = width
        self.height = height
        self.data = [
            [initialValue for y in range(height)]
            for x in range(width)
        ]
        if bitRepesentation:
            self._unpackBits(bitRepesentation)

    def __getitem__(self, i:int):
        return self.data[i]
    def __setitem__(self, key: int, item):
        self.data[key] = item
    def __str__(self):
        out = [
            [str(self.data[x][y])[0] for x in range(self.width)
        ] for y in range(self.height)
        ]
        out.reverse()
        return '\n'.join(''.join(x) for x in out)
    def __hash__(self) -> int:
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)
    def copy(self):
        g = Grid(self.width, self.height)
        # Remanipulate data in grid
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g


    def count(self, item=True) -> int:
        return sum([x.count(item) for x in self.data])

    def asList(self, key = True):
        l: List[Point] = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    l.append((x, y))
        return l


    def packBits(self) -> Tuple:
        """
        Return an efficient int list repesentation
        (width, height, bitPackedInts...)
        """
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currentInt)
                currentInt = 0
            bits.append(currentInt)
        return tuple(bits)
    def _cellIndexToPosition(self, index) -> Point:
        x = index / self.height
        y = index % self.height
        return x, y


    def _unpackBits(self, bits):
        """
        Fills data from a bit representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height:
                    break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1
    def _unpackInt(self, packed, size) -> List[bool]:
        bools = []
        if packed < 0:
            raise ValueError("Must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools
