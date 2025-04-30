from pacman import Directions
from game import Agent
import random
import game
import util

# Define a class for an agent that always turns left at intersections
class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    # Define method to get the action of the agent
    def getAction(self, state):
        # Get legal actions available to the agent
        legal = state.getLegalPacmanActions()
        # Get the current direction of the agent
        current = state.getPacmanState().configuration.direction
        # If the agent is currently stopped, set the direction to north
        if current == Directions.STOP:
            current = Directions.NORTH
        # Calculate the direction to the left of the current direction
        left = Directions.LEFT[current]
        # If the left direction is legal, turn left
        if left in legal:
            return left
        # If the current direction is legal, continue straight
        if current in legal:
            return current
        # If turning right is legal, turn right
        if Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]
        # If turning left from the left direction is legal, perform a U-turn
        if Directions.LEFT[left] in legal:
            return Directions.LEFT[left]
        # If none of the above actions are possible, stop
        return Directions.STOP

# Define a class for a greedy agent that chooses actions based on a provided evaluation function
class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    # Define method to get the action of the agent
    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        # Remove the STOP action if present
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # Generate successor states for each legal action
        successors = [(state.generateSuccessor(0, action), action)
                      for action in legal]
        # Evaluate each successor state using the evaluation function
        scored = [(self.evaluationFunction(state), action)
                  for state, action in successors]
        # Find the best score among the evaluated successor states
        bestScore = max(scored)[0]
        # Select actions that lead to the best score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # Choose a random action among the best actions
        return random.choice(bestActions)

# Define a simple evaluation function that returns the score of the state
def scoreEvaluation(state):
    return state.getScore()
