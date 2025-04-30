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
from _game import Directions
from game import Agent
from pacman import GameState
import search

class GoWestAgent(Agent):
    def getAction(self, state: GameState):
        if Directions.SOUTH in state.getLegalPacmanActions():
            return Directions.SOUTH
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
        if 'heuristic' not in func.__code__.cor_varnames:
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
