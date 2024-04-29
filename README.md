## Requirements:

numpy

pandas

seaborn

matplotlib.pyplot

## USAGE:

To test the code, Run the import statements at the top of Approach2, the q-learning function, and then you can adjust the 
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

## Approach2.ipynb

This is the main file, and contains the q-learning algorithm along with helper functions. 
It also contains sample runs which we used for our results, and the hyperparameters.

## Approach3.ipynb

This is last attempt at artificially training used high/low count decks



## Special_DECK.py

Adjusted deck code to either include high or low running count deck





