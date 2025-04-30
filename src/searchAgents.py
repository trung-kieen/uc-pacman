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
from inspect import Attribute
from typing import override
from _game import Directions
from game import Actions, Agent
from pacman import GameState
import search

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
    def __init__(self, fn = 'depthFirstSearch', prob = "PositionSearchProblem", heuristic="nullHeuristic"):
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
            # Get function from searchAgents.py
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
    A search problem defines the states space, start state, goal test, successor
    and cost function. This search problem cn be used to find paths to a
    particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.
    """

    def __init__(self, gameState: GameState, costFn = lambda x: 1,
                 goal = (1,1), start = None, warn=True, visualize=True):
        pass
        self.walls = gameState.getWalls()

        # Start pos
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print("Warning: this does not look like a regular search maze")

        # For display purpose
        self._visited = {}
        self._visitedlist = []
        self._expanded = 0



    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = self.goal == state
        if isGoal and self.visualize:
            # Log expanded list
            self._visitedlist.append(state)
            import __main__
            if '__display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__.display):
                    __main__.display.drawExpandedCells(self._visitedlist)

        return isGoal



    def getSuccessors(self, state):
        """
        Return successor states, the actions they require, and a cost of 1.

        As noted in search.py:
        For a given state, this could return a list of triples,
        (successor, action, stepCost), where 'successor' i a successor to
        the curent staste, 'action' is the action require to get there,
        and 'stepCost' is the incremental cost of expanding to that successor
        """



        successor = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successor.append((nextState, action, cost))
            # For display purpose
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)


    @override
    def getCostOfActions(self, actions):
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost
