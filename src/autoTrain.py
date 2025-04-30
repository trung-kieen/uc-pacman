import subprocess  # Importing the subprocess module to run external commands
import time
import numpy as np

# Setting the number of episodes to run
episodes = 5

# Looping through the episodes
for i in range(0, episodes):
    print("Running Episode", i)  # Printing the current episode number

    # Running the external command to execute a Pacman game and capturing the output
    result = subprocess.run("python pacman.py -p ReflexAgent -k 2 --frameTime 0", stdout=subprocess.PIPE)

    # Converting the stdout to a string
    test = str(result.stdout)

    # Initializing the win flag as 'Lose'
    winFlag = 'Lose'

    # Checking if the word 'victorious' exists in the output string
    if (test.find('victorious') != -1):
        winFlag = 'Win'  # Changing the win flag to 'Win' if Pacman is victorious

    # Loading weights from a CSV file
    weights = np.loadtxt("weights.csv", delimiter=",")

    # Appending weights and win flag to a text file named 'oldWeights.txt'
    with open('oldWeights.txt', 'a') as f:
        f.write(" ".join(map(str, weights)))  # Writing the weights as space-separated values
        f.write(' ' + winFlag)  # Adding the win flag after the weights
        f.write('\n')  # Adding a new line after each episode's entry
