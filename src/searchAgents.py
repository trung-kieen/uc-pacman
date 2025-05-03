# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

"""


import time
from typing import List, override
from game import Actions, Agent, Directions
from pacman import GameState
import search
import util

class GoWestAgent(Agent):
    def getAction(self, state: GameState):
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


class SearchAgent(Agent):
    """
    This very general search agent finds a path using supplied search algorithm for a
    supplied search problem. then return actions to follow that path.

    As a default, this agent run DFS on a PositionSearchProblem to find location (1,1)
    Options for fn include function define in this file like:
        depthFirstSearch or dfs
        breadthFirstSearch or bfs

    Or any other function implement the same interface
    """
    def __init__(self, fn = 'dfs', prob = "PositionSearchProblem", heuristic="nullHeuristic"):
        """
        # Warning: some advanced Python magic is employed blow to find the right functions and problems

        @paramm fn - main function use for searching
        @param prob - specific type of problem
        @param heuristic - use for determine good decision in A* and UCS


        Function and problem load function define in this file or search.py (for domain specific)
        Default use DFS and with no Heuristic function
        """
        self.fn = fn
        # Get search function from name and heurictic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search')

        # Get function from search.py
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print(("[SearchAgent] using funcion " + fn))
            self.searchFunction = func
        else:
            # Get heuristic function from searchAgents.py or search.py
            if heuristic in list(globals().keys()):
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py')
            print(('[SearchAgent] using function %s  and heuristic %s' % (fn, heuristic)))
            # Bind searchFunction with heuristic function
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in list(globals().keys()) or not prob.endswith("Problem"):
            raise AttributeError(prob + ' is not a search problem type in searchAgents.py')
        self.searchType: search.SearchProblem = globals()[prob]
        print(('[SearchAgent] using problem type ' + prob))


    def registerInitialState(self, state: GameState):
        """
        This is the first time that the agent see the layout of game board. Here,
        we choose a path to the goal. In this phase, the agent should compute the path to the goal
        and store it in the location variable.
        All of the work is done in this method!
        """
        if self.searchFunction == None: raise Exception("No search function provide for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state)
        self.actions = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print(("Path found with total cost of %d in %.1f seconds" % (totalCost, time.time() - starttime)))
        if ' _expanded' in dir(problem): print(('Search nodes expanded: %d' % problem._expanded))



    def getAction(self, state: GameState):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).
        Return Directions.STOP if there is no further action to take.
        """

        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
    """
    Stores the start and goal

    """
    def __init__(self, gameState, costFn = lambda x: 1, goal = (1,1), start= None, warn = True, visualize=True) -> None:
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.stateState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print("Warning: this does not look like a regular search maze")


        self._visited = { }
        self._visitedlist = []
        self._expanded = 0

    def getStartState(self):
        return self.startState


    def isGoalState(self, state):
        isGoal = state == self.goal

        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):
                    __main__._display.drawExpandedCells(self._visitedlist)

        return isGoal

    def getSuccessors(self, state) -> List:
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class FoodSearchProblem:
    """
    Search for all food in game

    State use in this problem is a tuple (pacmanPosition, foodGrid)
    where pacmanPosition: a tutple (x, y) of integer specifying Pacman's position
    foodGrid: a composition class Grid (2d) of bool to check exist food or node
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {}

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """
        successors= []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y+dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """
        REturn the cost of particular sequence of actions. If those actions
        include an illagal move, return 999999
        """
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 99999
            cost += 1
        return cost


class ClosestDotSearchAgent(SearchAgent):
    def registerInitialState(self, state ):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception("findPathToClosestDot return an illgal move: %s!\n%s" % (t))

                # Get next state by on execute action
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print("Path found with cost %d." % len(self.actions))



    def findPathToClosestDot(self, gameState):
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        # TODO: inject from command line
        return search.bfs(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for find a path to any food.

    Just like PositionSearchProblem, but has a different goal test,
    which you need to fill in below. The state space and
    successor function not need to be change
    """

    def __init__(self, gameState) -> None:
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited = { }
        self._visitedlist = []
        self._expanded = 0

    @override
    def isGoalState(self, state):
        x, y = state
        return self.food[x][y]




def foodHeuristic(state, problem):
    """Encourage Pacman to eat all the pellets as fast as possible."""
    position, foodGrid = state

    heuristic = 0
    foodList = foodGrid.asList()

    #calculate the distance from current node to food-containing nodes
    if len(foodList) > 0:
        closestPoint = findClosestPoint(position, foodList)
        farthestPoint = findFarthestPoint(position, foodList)

        closestPointIndex = closestPoint[0]
        farthestPointIndex = farthestPoint[0]

        currentNode = problem.startingGameState
        closestFoodNode = foodList[closestPointIndex]
        farthestFoodNode = foodList[farthestPointIndex]

        #distance between current location and closest manhattan node
        currentToClosest = mazeDistance(position, closestFoodNode, currentNode)

        #distance between closest manhattan node and farthest manhattan node
        closestToFarthest = mazeDistance(closestFoodNode, farthestFoodNode, currentNode)

        heuristic = currentToClosest + closestToFarthest

    return heuristic


def findClosestPoint(location, goalArray):
    """
    Helper function for corners
    """

    closestPoint = 0
    closestPointCost = util.manhattanDistance( location, goalArray[0] )

    for j in range(len(goalArray)):
        #calculate distance between current state to corner
        cornerLocation = goalArray[j]
        lengthToCorner = util.manhattanDistance( location, cornerLocation )

        if lengthToCorner < closestPointCost:
            closestPoint = j
            closestPointCost = lengthToCorner

    return (closestPoint, closestPointCost)

def findFarthestPoint(location, goalArray):
    """
    Helper function for corners
    """

    farthestPoint = 0
    farthestPointCost = util.manhattanDistance( location, goalArray[0] )

    for j in range(len(goalArray)):
        #calculate distance between current state to corner
        cornerLocation = goalArray[j]
        lengthToCorner = util.manhattanDistance( location, cornerLocation )

        if lengthToCorner > farthestPointCost:
            farthestPoint = j
            farthestPointCost = lengthToCorner

    return (farthestPoint, farthestPointCost)



def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
