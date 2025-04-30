
# search.py
# ---------
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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here



from inspect import isgenerator, ismemberdescriptor
from game import Directions
from pacman import GameState
import searchAgents
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Return true if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        For a givent state, this should return a list of triples, (successor,
        action, stepCost), where the successor to the current state,
        'action' is the action required to get there,
        and 'stepCost' is the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()
    def getCostOfActions(self, actions) -> int:
        """
        Return total cost to particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()
        return 0

def tinyMazeSearch(problem):
    """
    Return a sequence of moves that solves tinyMaze. For any other maze, the sequence
    of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]



def dfs(problem:  SearchProblem):
    """
    problem - PositionSearchProblem that implement SearchProblem
    """

    frontier = util.Stack()
    explored = set()
    startState = problem.getStartState()
    startNode = (startState, [], 0)
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        if problem.isGoalState(currentState):
            return actions

        # Explore

        if currentState not in explored:
            explored.add(currentState)
            for (newState, newAction, preCost) in problem.getSuccessors(currentState):
                child_node = (newState, actions + [newAction], preCost + 1)
                frontier.push(child_node)
    return [Directions.SOUTH]



def bfs(problem:  SearchProblem):
    """
    problem - PositionSearchProblem that implement SearchProblem
    """

    frontier = util.Queue()
    explored = set()
    startState = problem.getStartState()
    startNode = (startState, [], 0)
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        if problem.isGoalState(currentState):
            return actions

        # Explore

        if currentState not in explored:
            explored.add(currentState)
            for (newState, newAction, preCost) in problem.getSuccessors(currentState):
                child_node = (newState, actions + [newAction], preCost + 1)
                frontier.push(child_node)
    return [Directions.SOUTH]




# def closestDotSearch(problem:  SearchProblem):
#     """
#     problem - PositionSearchProblem that implement SearchProblem
#     """

#     problem.
#     frontier = util.Queue()
#     explored = set()
#     startState = problem.getStartState()
#     startNode = (startState, [], 0)
#     frontier.push(startNode)
#     while not frontier.isEmpty():
#         currentState, actions, currentCost = frontier.pop()
#         if problem.isGoalState(currentState):
#             return actions

#         # Explore

#         if currentState not in explored:
#             explored.add(currentState)
#             for (newState, newAction, preCost) in problem.getSuccessors(currentState):
#                 child_node = (newState, actions + [newAction], preCost + 1)
#                 frontier.push(child_node)
#     return [Directions.SOUTH]
