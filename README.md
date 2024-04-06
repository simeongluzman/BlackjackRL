test1.ipynb contains the initial test for interacting with the blackjack env in the gym library, just so we understand how the environment works b4 we move on to making the logic for the agent. 

To test it, install the libraries in the requirements.txt file and try running the box below. If you have issues  w installation (i had a few), just ask chatgpt and it will help. i needed to install a lib called swig. 


##  TODO

1. Change blackjack gym env (lines 178-181 in blackjack.py) in order to print which cards dealer draws after player stays (just for info/debugging, kind of wierd they didn't already implement that)
2. Instead of interacting via keyboard, we will be training an agent to decide what to do (RL learning, where agent will be rewarded/punished for winning/losing rounds)
3. add more functionality to blackjack env such as:
    - Splitting cards
    - Doubling down

3. We also need to come up with some benchmark comparisons, such as randomly choosing hit/stay, and see how that does compared to a slightly better strategy, and finally compared to our agent/agents 

4. If time allows, we should completely change how the env works. right now, it simply picks a card at random with replacement, so there is no accurate model checking which cards have already been played, and there is no logic for 'shuffling' the deck after a certain amount of rounds
