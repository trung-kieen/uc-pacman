# Modify by: Vi, Chien
# Licensing following UC Berkele


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from typing import List, Tuple, Any
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import pacman

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        if self.actions == None:
            self.actions = []
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
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
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
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

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState: pacman.GameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

class MSTCalculator:
    """Class to calculate Minimum Spanning Tree weight using Kruskal's algorithm with Union-Find."""
    
    def __init__(self):
        self.parent = []
        self.rank = []
    
    def find(self, parent: list[int], u: int) -> int:
        """Tìm gốc của tập hợp chứa u với nén đường (path compression)."""
        if parent[u] != u:
            parent[u] = self.find(parent, parent[u])
        return parent[u]
    
    def union(self, parent: list[int], rank: list[int], u: int, v: int):
        """Hợp nhất hai tập hợp chứa u và v, sử dụng union by rank."""
        pu = self.find(parent, u)
        pv = self.find(parent, v)
        
        if pu == pv:
            return
        
        if rank[pu] < rank[pv]:
            parent[pu] = pv
        elif rank[pu] > rank[pv]:
            parent[pv] = pu
        else:
            parent[pv] = pu
            rank[pu] += 1
    
    def calculate_mst_weight(self, nodes: list[tuple[int, int]], distance_func, cache: dict) -> float:
        """
        Tính trọng số MST của danh sách các node sử dụng hàm khoảng cách cho trước.
        
        Args:
            nodes: Danh sách các node (tọa độ).
            distance_func: Hàm tính khoảng cách giữa hai node.
            cache: Từ điển lưu trữ khoảng cách để tái sử dụng.
        
        Returns:
            Trọng số MST.
        """
        if len(nodes) <= 1:
            return 0
        
        # Tạo danh sách cạnh
        edges = []
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                key = tuple(sorted([node1, node2]))
                if key not in cache:
                    cache[key] = distance_func(node1, node2)
                dist = cache[key]
                edges.append((dist, i, j))
        
        # Sắp xếp cạnh theo khoảng cách
        edges.sort()
        
        # Khởi tạo Union-Find
        self.parent = list(range(len(nodes)))
        self.rank = [0] * len(nodes)
        mst_weight = 0
        
        # Xây dựng MST
        for dist, u, v in edges:
            if self.find(self.parent, u) != self.find(self.parent, v):
                self.union(self.parent, self.rank, u, v)
                mst_weight += dist
        
        return mst_weight
    
def findClosestPoint(location, goalArray):
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

def foodHeuristic(state: Tuple[Tuple[int, int], List[List[bool]]], problem: 'FoodSearchProblem') -> float:
    """
    Hàm heuristic cho FoodSearchProblem, sử dụng MST và khoảng cách đến viên thức ăn gần nhất.
    
    Args:
        state: Tuple chứa (position, foodGrid), position là tọa độ Pacman, foodGrid là lưới thức ăn.
        problem: Đối tượng FoodSearchProblem, chứa startingGameState và heuristicInfo.
    
    Returns:
        Giá trị heuristic.
    """
    position, foodGrid = state
    foodList = foodGrid.asList()
    
    if len(foodList) == 0:
        return 0
    
    # Tìm viên thức ăn gần nhất
    closest_distance = float('inf')
    for food in foodList:
        key = (position, food)
        if key not in problem.heuristicInfo:
            problem.heuristicInfo[key] = mazeDistance(position, food, problem.startingGameState)
        dist = problem.heuristicInfo[key]
        closest_distance = min(closest_distance, dist)
    
    # Tính MST bằng MSTCalculator
    mst_calculator = MSTCalculator()
    mst_weight = mst_calculator.calculate_mst_weight(
        nodes=foodList,
        distance_func=lambda x, y: mazeDistance(x, y, problem.startingGameState),
        cache=problem.heuristicInfo
    )
    
    # Giá trị heuristic là tổng khoảng cách gần nhất và trọng số MST
    heuristic = closest_distance + mst_weight
    return heuristic

def closestToFartherHeuristic(state, problem):
    """Encourage Pacman to eat all the pellets as fast as possible."""
    position, foodGrid = state
    heuristic = 0
    foodList = foodGrid.asList()
    
    # Khởi tạo heuristicInfo nếu chưa có
    if not hasattr(problem, 'heuristicInfo'):
        problem.heuristicInfo = {}
    
    #calculate the distance from current node to food-containing nodes
    if len(foodList) > 0:
        closestPoint = findClosestPoint(position, foodList)
        farthestPoint = findFarthestPoint(position, foodList)
        
        closestPointIndex = closestPoint[0]
        farthestPointIndex = farthestPoint[0]
        
        currentNode = problem.startingGameState
        closestFoodNode = foodList[closestPointIndex]
        farthestFoodNode = foodList[farthestPointIndex]
        
        key1 = (position,closestFoodNode)
        if key1 not in problem.heuristicInfo:
            problem.heuristicInfo[key1] =  mazeDistance(position, closestFoodNode, currentNode)
        currentToClosest = problem.heuristicInfo[key1]

        key2 = (position,farthestFoodNode)
        if key2 not in problem.heuristicInfo:
            problem.heuristicInfo[key2] =  mazeDistance(position, farthestFoodNode, currentNode)
        currentToFarthest = problem.heuristicInfo[key2]
        
        # #distance between current location and closest manhattan node
        # currentToClosest = mazeDistance(position, closestFoodNode, currentNode)
        
        # #distance between closest manhattan node and farthest manhattan node
        # closestToFarthest = mazeDistance(closestFoodNode, farthestFoodNode, currentNode)

        heuristic = currentToClosest + currentToFarthest
    return heuristic


class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState: pacman.GameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mazeDistance(point1: Tuple[int, int], point2: Tuple[int, int], gameState: pacman.GameState) -> int:
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
