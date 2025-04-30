import subprocess  # Importing the subprocess module to run external commands
import time
import numpy as np

# Setting the number of episodes to run
episodes = 100

# Looping through the episodes
for i in range(0, episodes):
    print("Running Episode", i)  # Printing the current episode number

    # Running the external command to execute a Pacman game and capturing the output
    result = subprocess.run("python pacman.py -p ReflexAgent -l mediumClassic --frameTime 0", stdout=subprocess.PIPE)

    # Converting the stdout to a string
    test = str(result.stdout)

    # Initializing the win flag as 'Lose'
    winFlag = 'Lose'

    # Checking if the word 'victorious' exists in the output string
    if (test.find('victorious') != -1):
        winFlag = 'Win'  # Changing the win flag to 'Win' if Pacman is victorious

    # Appending the win flag to a text file named 'WinRatio.txt'
    with open('WinRatio.txt', 'a') as f:
        f.write(winFlag)  # Writing the win flag
        f.write('\n')  # Adding a new line after each win/loss entry
