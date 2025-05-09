# Modify by: Kien, Duong
# Licensing following UC Berkele


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from backend import ReplayMemory

import backend
import gridworld


import random,util,math
import numpy as np
import copy

class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.q_values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.q_values[state, action]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state return a value of 0.0.
        """
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        max_value = float("-inf")
        for action in actions:
            q_value = self.getQValue(state, action)
            max_value = max(q_value, max_value)
        return max_value


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state just return None.
        """
        qValuesToActions= {self.getQValue(state, action): action for action in self.getLegalActions(state)}
        max_q_values = max(qValuesToActions.keys())
        max_q_actions = [qValuesToActions[value] for value in qValuesToActions.keys() if value == max_q_values]
        if max_q_actions:
            return random.choice(max_q_actions)
        else:
            return None




    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state function return None
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        rational_action = self.computeActionFromQValues(state)
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return rational_action

    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          Q-Value update here
        """
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        self.q_values[state, action] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

class ApproximateQAgent(PacmanQAgent):
    """
       Only have to overwrite getQValue and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        feature_vector = self.featExtractor.getFeatures(state, action)
        q_value = 0.0
        for feat in feature_vector.keys():
            q_value += feature_vector[feat] * self.weights[feat]

        return q_value


    def update(self, state, action, nextState, reward: float):
        """
           Update weights based on transition
        """
        max_q_next_action = float("-inf")
        for next_action in self.getLegalActions(state):
            max_q_next_action = max(max_q_next_action, self.getQValue(nextState, next_action))
        if max_q_next_action == float("-inf"): max_q_next_action = 0

        current_q_value = self.getQValue(state, action)
        diff = (reward + (self.discount * max_q_next_action)) - current_q_value

        feature_vector = self.featExtractor.getFeatures(state, action)

        temp_weight = util.Counter()
        for w_i in self.weights:
            self.weights[w_i] = self.weights[w_i] + self.alpha * diff * feature_vector[w_i]



    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # For bugging at the end of episodes
            pass
