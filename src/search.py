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
    

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
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
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
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
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """  
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    # Create frontier
    frontier = util.PriorityQueue()
    explored_to_min_cost = dict() # this dict will store the minimum cost reached of each state that has been explored
    # Storage explored node to keep track minium value
    start_state = problem.getStartState()
    start_actions = []
    start_cost = 0

    # Add stater node to frontier
    start_node = (start_state, start_actions, start_cost)
    frontier.push(start_node, start_cost)

    # Graph search until open list is empty
    while not frontier.isEmpty():
        cur_state, cur_actions, cur_cost = frontier.pop()

        # Check if current node is goal => return actions
        if problem.isGoalState(cur_state):
            return cur_actions
        

        # Check if node is not explore or better cost
        if cur_state not in explored_to_min_cost or explored_to_min_cost[cur_state] > cur_cost:
            # Mark node as explored and update the better cost (if already exist)
            explored_to_min_cost[cur_state] = cur_cost
            # Expand node nearby
            for succ_state, action , succ_cost in problem.getSuccessors(cur_state):

                succ_actions = cur_actions + [action]
                g_cost = cur_cost + succ_cost
                h_cost = g_cost + heuristic(succ_state, problem)

                # NOTE: node information should contain about g_cost to track current cost without heuristic
                succ_node = (succ_state, succ_actions, g_cost)
                # Use h_cost for heapq priority
                frontier.push(succ_node, h_cost)

    return []

def trackAStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    import util

    # Create frontier
    frontier = util.PriorityQueue()
    explored_to_min_cost = dict()

    # Storage explored node to keep track minium value
    start_state = problem.getStartState()
    start_actions = []
    start_cost = 0

    # Add starter node to frontier
    start_node = (start_state, start_actions, start_cost)
    frontier.push(start_node, start_cost)

    step = 0  # để theo dõi vòng lặp

    # Graph search until frontier is empty
    while not frontier.isEmpty():
        cur_state, cur_actions, cur_cost = frontier.pop()
        
        print(f"Expanded node: {cur_state}")

        print(f"\n--- Step {step} ---")
        print(f"Pop node: {cur_state}, g(n) = {cur_cost}, path = {cur_actions}")

        # Check if current node is goal => return actions
        if problem.isGoalState(cur_state):
            print("Reached goal!")
            return cur_actions
        print("HAVE NOT REACHED GOAL! ")
        # Check if node is not explored or has a better cost
        if cur_state not in explored_to_min_cost or explored_to_min_cost[cur_state] > cur_cost:
            # Mark node as explored
            explored_to_min_cost[cur_state] = cur_cost

            # Expand node
            for succ_state, action, succ_cost in problem.getSuccessors(cur_state):
                succ_actions = cur_actions + [action]
                g_cost = cur_cost + succ_cost
                h_cost = heuristic(succ_state, problem)
                f_cost = g_cost + h_cost

                succ_node = (succ_state, succ_actions, g_cost)

                print(f"  Successor: {succ_state}, action: {action}, g(n): {g_cost}, h(n): {h_cost}, f(n): {f_cost}")

                frontier.push(succ_node, f_cost)

        # In toàn bộ các node đã explore
        print("  Explored nodes so far:")
        for state, cost in explored_to_min_cost.items():
            print(f"    {state}, g(n): {cost}")
            
            
        # In frontier sau mỗi vòng lặp
        print("  Frontier:")
        for item in frontier.heap:
            state, actions, g_cost = item[2]  # item = (priority, count, (state, actions, g))
            f_cost = item[0]
            print(f"    {state}, f(n): {f_cost}, path: {actions}")

        step += 1

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
