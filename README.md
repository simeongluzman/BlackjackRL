## Requirements:

numpy
pandas
seaborn
matplotlib.pyplot

## USAGE:

To test the code, Run the import statements at the top of DataV3, the q-learning function, and then you can adjust the 
hyperparameters and try extracting a policy. 


## DECK.py

This file is used to simulate the blackjack table, and allows player to make moves. 
Example Usage:

table = Deck.BlackJackEnv(5)
table.start_round()
table.next(0) 0 for stand, 1 for hit 2 for double down
Both start_round and next return: player hand, dealer hand, hasAce, roundStarted, reward, runningCount, hasDoubled

## PolicyH.py

This file contains the helper functions to visualize policy outputs and also the try_policy function to evaluate a policy in a long simulation. 

## DataV3.ipynb

This is the main file, and contains the q-learning algorithm along with helper functions. 
It also contains sample runs which we used for our results, and the hyperparameters.


## rewards-deck.txt

Contains results from running card-counting agent on different numbers of decsk




