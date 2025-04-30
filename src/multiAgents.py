from util import manhattanDistance
from game import Directions
import random, util
import numpy as np
import math
from util import Stack
from game import Agent

class Node:

    def __init__(self, state, parent, action, path_cost):
        # Node constructor
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    """

    def goalTest(self, gs, pos, flag):
        # Testing for goals
        if(flag == 0):
            if(gs.hasFood(pos[0], pos[1])):
                return True
            return False
        if(flag == 1):
            gpos = gs.getGhostPositions()
            for gp in gpos:
                if(gp == pos):
                    return True
            return False
        

    def DLS(self, currentNode, stack, explored, layer, limit, found, flag):
        # Depth Limited Search
        explored.append(currentNode)
        if(self.goalTest(currentNode.parent.state, currentNode.state.getPacmanPosition(), flag)):
            stack.push(currentNode)
            return stack, explored, True
        if(layer == limit):
            return stack, explored, False
        stack.push(currentNode)
        actions = currentNode.state.getLegalActions()
        for a in actions:
            newState = currentNode.state.generatePacmanSuccessor(a)
            newNode = Node(newState, currentNode, a, 1)
            if newNode in explored:
                continue
            stack, explored, found = self.DLS(newNode, stack, explored, layer+1, limit, found, flag)
            if(found):
                return stack, explored, True
        stack.pop()
        return stack, explored, False
    
    def IDS(self, sgs, limit, flag):
        # Iterative Deepening Search
        found = False
        current_limit = 0
        while(not found and current_limit <= limit):
            current_limit = current_limit + 1
            startNode = Node(sgs, None, None, 0)
            startNode.parent = startNode
            stack = Stack()
            explored = []
            stack, explored, found = self.DLS(startNode, stack, explored, 1, current_limit, False, flag)

        actions = []
        while(not stack.isEmpty()):
            node = stack.pop()
            actions.append(node.action)

        if not actions:
            return actions, found
        
        actions.reverse()
        actions.pop(0)  # Removes start node from actions

        return actions, found


    def getAction(self, gameState):
        """
        Choose an action based on evaluation function.
        """
        legalMoves = gameState.getLegalActions()

        weights = np.loadtxt("weights.csv", delimiter=",")

        scores = []
        for action in legalMoves:
            s = self.evaluationFunction(gameState, action, weights)
            scores.append(s)
        
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def CalcGhostPos(self, cgs, actions):
        # Calculate ghost position
        for a in actions:
            cgs = cgs.generatePacmanSuccessor(a)
        return cgs.getPacmanPosition()

    def findAllGhosts(self, cgs):
        # Find all active and scared ghosts and then turn them into binary features
        f1 = 0  # Active ghost one step away (Binary)
        f2 = 0  # Active ghost two steps away (Binary)
        f3 = 0  # Scared ghost one step away (Binary)
        f4 = 0  # Scared ghost two steps away (Binary)
        actions, found = self.IDS(cgs, 3, 1)
        if not found:
            return f1, f2, f3, f4
        ghosts = cgs.getGhostStates()
        ghostPos = self.CalcGhostPos(cgs, actions)
        foundGhostPosition = False
        for g in ghosts:
            if(ghostPos == g.configuration.pos):
                ghost = g
                foundGhostPosition = True
                break
        
        if not foundGhostPosition:
            return f1, f2, f3, f4

        if(ghost.scaredTimer > 0):  # If ghost is scared
            if(len(actions) <= 1):
                f3 = 1
            if(len(actions) == 2):
                f4 = 1
        if(ghost.scaredTimer == 0): # If ghost is active
            if(len(actions) <= 1):
                f1 = 1
            if(len(actions) == 2):
                f2 = 1

        return f1, f2, f3, f4
        
    def getFeatureFive(self, cgs, sgs):
        # Eating Food (Binary)
        if(self.goalTest(cgs, sgs.getPacmanPosition(), 0)):
            return 1
        return 0

    def getFeatureSix(self, cgs):
        # Distance to closest food
        food = cgs.getFood()
        pacPos = cgs.getPacmanPosition()
        dist = []
        x_size = food.width
        y_size = food.height
        for x in range(0, x_size):
            for y in range(0, y_size):
                if(food[x][y] == True):
                    dist.append(manhattanDistance(pacPos, (x,y)))
        if not dist:
            return 0
        closestFood = min(dist)
        return 1/closestFood   

    def evaluationFunction(self, currentGameState, action, weights):
        # Evaluation function for choosing actions
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        f1, f2, f3, f4 = self.findAllGhosts(successorGameState)
        f5 = self.getFeatureFive(currentGameState, successorGameState)
        f6 = self.getFeatureSix(successorGameState)
        features = np.array([f1, f2, f3, f4, f5, f6])

        Q_s_a = np.dot(weights, np.transpose(features))

        return Q_s_a

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function returns the score of the state.
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    """
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
