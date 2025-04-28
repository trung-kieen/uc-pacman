from typing import List, Literal, NamedTuple, NoReturn, Self, Tuple, overload, override
import time
import os
import traceback
import sys
import util
from util import nearestPoint


# Agent speed can be floating point number so dx, dy is also floating point number
AgentPoint = Tuple[float, float]
GridPoint = Tuple[int, int]

class Agent:
    def __init__(self, index = 0):
        self.index = index


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {
        NORTH: WEST,
        SOUTH: EAST,
        EAST : NORTH,
        WEST: SOUTH,
        STOP: STOP
    }


    RIGHT = dict([(y, x) for x , y in list(LEFT.items())])

    REVERSE = {
        NORTH: SOUTH,
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
        self.pos:AgentPoint =  pos
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
    Agent for pacman agent is direction
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
    def vectorToDirection(vector: AgentPoint):
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
        """
        Return a list of possible action (direction) for agent to move
        """
        possible = []
        x, y = config.pos
        # Get position of nearest position between 2 grid
        x_grid_nearest, y_grid_nearest = int(x + 0.5), int(y + 0.5)

        """
        For smooth transition we use float to store agent configuration as float instead of int
        Only allow agent to change direction when the absoluate distance less than tolerance
        Otherwise must keep same agent direction
        """
        if (abs(x - x_grid_nearest) + abs(y - y_grid_nearest)) > Actions.TOLERANCE:
            return [config.getDirection()]
        for direction, vector in Actions._directionsAsList:
            dx, dy = vector
            next_y = y_grid_nearest + dy
            next_x = x_grid_nearest + dx
            if not walls[next_x][next_y]:
                possible.append(direction)
        return possible
    @staticmethod
    def getLegalNeighbors(position: AgentPoint, walls):
        """
        Return a list of neighbors point that not out of bound
        """
        x, y = position
        x_grid_nearest, y_grid_nearest = int(x + 0.5), int(y + 0.5)
        neighbors = []
        for direction, vector in Actions._directionsAsList:
            dx, dy = vector
            next_x = x_grid_nearest + dx
            next_y = y_grid_nearest + dy
            if next_x < 0 or next_x == walls.width:
                continue
            if next_y < 0 or next_y == walls.width:
                continue

            valid_neighbor = not walls[next_x][next_y]
            if valid_neighbor:
                neighbors.append((next_x, next_y))
        return neighbors

    @staticmethod
    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)



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
        self.isPacman: bool = isPacman
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
    def getPosition(self) -> None | AgentPoint:
        if self.configuration == None:
            return None
        return self.configuration.getPosition()
    def getDirection(self):
        if self.configuration:
            return self.configuration.getDirection()

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

        # Reuse Grid to display agent str => use union of int | str
        self.data: List[List[int | str]] = [
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
        """
        Return list agent point in order of 2d iteration
        """
        l: List[AgentPoint] = []
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
    def _cellIndexToPosition(self, index) -> GridPoint:
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


class GameStateData:
    def __init__(self, prevState: Self | None) -> None:
        """
        Generate new data packet by copying information from its predecessor.
        """
        if prevState != None:
            self.food= prevState.food
            self.capsules: List= prevState.capsules[:]
            self.agentStates: List[AgentState] = self.copyAgentStates(prevState.agentStates)
            self.layout = prevState.layout
            self._eaten: List[bool] = prevState._eaten
            self.score: int = prevState.score


        self._foodEaten = None
        self._foodAdded = None
        self._capsulesEaten = None
        self._agentMoved = None
        self._wind = False
        self._lose = False
        self.scoreChange = 0

    def deepCopy(self):
        state = GameStateData(self)
        state.food = self.food.deepCopy()
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        state._foodEaten = self._foodEaten
        state._foodAdded = self._foodAdded
        state._capsulesEaten = self._capsulesEaten
        return state

    def copyAgentStates(self, agentStates: List[AgentState]):
        copiedStates: List[AgentState] = []
        for agentState in agentStates:
            copiedStates.append(agentState.copy())
        return copiedStates

    # TODO: fill layout class name
    def initialize(self, layout, numGhostAgents):
        """
        Creates an ginitial aem state from a layout game state from layout array (see layout.py)
        """
        self.food = layout.food.copy()
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.scoreChange = 0
        self.agentStates = []
        numGhosts = 0
        for isPacman, pos in layout.agentPositions:
            if not isPacman:
                # Skip create ghost if enough
                if numGhosts == numGhostAgents:
                    continue
                else:
                    numGhosts += 1
            # Create new pacman/ghost agent
            self.agentStates.append(
                AgentState(
                    Configuration(pos, Directions.STOP), isPacman
                )
            )
        self._eaten = [False for _ in self.agentStates]


    @override
    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        if not isinstance(other, GameStateData):
            return False
        if not self.agentStates == other.agentStates:
            return False
        if not self.food == other.food:
            return False
        if not self.capsules == other.capsules:
            return False
        if not self.score == other.score:
            return False
        return True
    @override
    def __hash__(self) -> int:
        """
        Allow use state in hash, set
        """

        for state in self.agentStates:
            try:
                int(hash(state))
            except TypeError as e:
                print(e)
        return int(
                (hash(tuple(self.agentStates))
                + 13 * hash(self.food)
                + 113 * hash(tuple(self.capsules)) + 7 * hash((self.score)))
                % 1048575)
    @override
    def __str__(self) -> str:
        width, height = self.layout.width, self.layout.height
        map = Grid(width, height)
        # TODO: reconstituteGrid from packedBit
        # if type(self.food) == type ((1, 2)):
        #     self.food = reconstituteGrid(self.food)
        for x in range(width):
            for y in range(height):
                food, walls = self.food, self.layout.walls
                map[x][y] = self._foodWallStr(food[x][y], walls[x][y])

        for agentState in self.agentStates:
            if agentState == None:
                continue
            if agentState.configuration == None:
                continue
            # TODO: create nearestPoint function in util
            x, y = [int(i) for i in nearestPoint(agentState.configuration.pos)]
            agent_direction = agentState.configuration.direction
            if agentState.isPacman:
                map[x][y] = self._pacStr(agent_direction)
            else:
                map[x][y] = self._ghostStr(agent_direction)

        for x, y in self.capsules:
            map[x][y] = 'o'
        return str(map) + ("\nScore: %d\n" % self.score)


    def _foodWallStr(self, hasFood, hasWall) -> str:
        if hasFood:
            return "."
        elif hasWall:
            return "%"
        else:
            return ' '

    def _pacStr(self, dir):
        """
        Pacman reperesent by his mouth
        """
        if dir == Directions.NORTH:
            return "v"
        elif dir == Directions.SOUTH:
            return "^"
        elif dir == Directions.WEST:
            return ">"
        else:
            return "<"
    def _ghostStr(self, dir):
        return "G"


class Game:
    """
    Game manages the flow, agents
    """

    OLD_STDOUT = None
    OLD_STDERR = None

    def __init__(self, agents, display, rules, startingIndex = 0, muteAgents = False, catchExceptions = False) -> None:
        self.agents: List[Agent] = agents
        self.agentCarshed = False
        self.display = display
        # TODO: class name for rule
        self.rules = rules
        self.startingIndex = startingIndex
        self.gameOver = False
        self.muteAgents = muteAgents
        self.catchExceptions = catchExceptions
        self.moveHistory = []
        self.totalAgentTimes = [0 for _ in agents]
        self.totalAgentTimeWarnings = [0 for _ in agents]
        self.agentTimeout = False
        import io
        self.agentOutput = [io.StringIO() for agent in agents]


    def getProgress(self):
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    def _agentCrash(self, agentIndex, quite=False):
        """Helper method for handling agent crashes"""
        if not quite:
            traceback.print_exc();
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCarshed(self, agentIndex)

    def mute(self, agentIndex):
        if not self.muteAgents:
            return

        global OLD_STDOUT, OLD_STDERR
        import io
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agentOutput[agentIndex]
        sys.stderr = self.agentOutput[agentIndex]


    def unmute(self):
        """TODO: explain"""
        if not self.muteAgents:
            return
        global OLD_STDOUT, OLD_STDERR

        # Revert stdout/stderr to originials
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    def run(self):
        """
        Main control loop for game play
        """
        self.display.initialize(self.state.data)
        self.numMoves = 0


        # for i in range(len(self.agents)):
        #     agent = self.agents[i]
        #     if not agent:
        #         self.mute(i)
        #         print("Agent %d failed to load" %i, file=sys.stderr)
        #         self.unmute()
        #         self._agentCrash(i, quite=True)
        #         return
        #     if ("registerIntialState" in dir(agent)):
        #         self.mute(i)
        #         if self.catchExceptions:
        #             try:
        #                 timed_func = TimeoutFunction (
        #                 agent.registerIntialState, int(self.rules.getMaxStartupTIme(i))

            # TODO





try:
    # Share cpu/gpu
    import boinc
    _BOINC_ENABLED = True
except
    _BOINC_ENABLED = False
