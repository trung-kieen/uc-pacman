Hands on Artificial Intelligence algorithms in a real game

Search: DFS, BFS, A*

MDPs:  
- Value iteration 

Reinforcement learning: 
- Q-learning 
- Approximate Q-learning 

# Setup 
1. Navigate to `src` 
2. Active env in linux environment 
```shell 
python3 -m venv env36 && source env36/bin/activate
```
3. Install dependencies
```
pip install -Ur requirements.txt
```


4. Start project with main entry `pacman.py`

```bash 
# Search algorithms
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
python pacman.py -l mediumScaryMaze -p SearchAgent -a fn=astar
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic


# Compare heuristic
python pacman.py -l mediumCompareHeuristic -p SearchAgent -a fn=aStarSearch,heuristic=manhattanHeuristic
python pacman.py -l mediumCompareHeuristic -p SearchAgent -a fn=aStarSearch,heuristic=euclideanHeuristic


python pacman.py -l testSearch -p AStarFoodSearchAgent
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

```bash 
# Mdps 
python gridworld.py -a value -i 100 -k 10
python gridworld.py -a value -i 5
```


```bash 
# RL
python gridworld.py -a q -k 5 -m
python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
```

# Acknowledgement
Most of our work involve in those files: `search.py`, `searchAgents.py`, `valueIterationAgents.py` and `qlearningAgents.py`

