import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Deck


def map_policies(policies, countCards):
    # Constants
    player_values = list(range(4, 22))
    dealer_cards = list(range(2, 12))
    # Hard Coded Optimal Strategy for comparison with Q-learning:
    # SOURCE: https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

    strat = []
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'])
    strat.append(['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
    strat.append(['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    # Insert the hardcoded optimal policy at the beginning of the list
    pols = []
    if countCards:
        pols.append(policies[1])
        pols.append(strat)
        pols.append(policies[0])
        pols.append(policies[2])

        # Create subplots in a 2x2 layout
        fig, axes = plt.subplots(2, 2, figsize=(8, 8), sharey=True)
        axes = axes.flatten()  # Flatten the 2D array of axes into 1D for easier indexing

        for idx, policy in enumerate(pols):
            # Map 'H' to 0, 'S' to 1, and 'D' to 2 for numerical representation
            strategy_numerical = [[0 if cell == 'H' else 1 if cell ==
                                   'S' else 2 if cell == 'D' else cell for cell in row] for row in policy]
            strategy_df = pd.DataFrame(
                policy, index=player_values, columns=dealer_cards)
            strategy_df_numerical = pd.DataFrame(
                strategy_numerical, index=player_values, columns=dealer_cards)

            # Plot each heatmap in its subplot
            sns.heatmap(strategy_df_numerical, annot=strategy_df,
                        cmap='YlGnBu', fmt='', cbar=False, ax=axes[idx])
            title = ['Neutral Policy', 'Optimal Policy',
                     'Policy for running count < -2', 'Policy for running count > +2'][idx]
            axes[idx].set_title(title)
            axes[idx].set_xlabel("Dealer's Face-Up Card")
            axes[idx].set_ylabel("Player's Total" if idx % 2 == 0 else "")

        plt.tight_layout()
        plt.show()
    else:
        pols.append(policies)
        pols.append(strat)
        fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
        axes = axes.flatten()

        for idx, policy in enumerate(pols):
            # Map 'H' to 0, 'S' to 1, and 'D' to 2 for numerical representation
            strategy_numerical = [[0 if cell == 'H' else 1 if cell ==
                                   'S' else 2 if cell == 'D' else cell for cell in row] for row in policy]
            strategy_df = pd.DataFrame(
                policy, index=player_values, columns=dealer_cards)
            strategy_df_numerical = pd.DataFrame(
                strategy_numerical, index=player_values, columns=dealer_cards)

            # Plot each heatmap in its subplot
            sns.heatmap(strategy_df_numerical, annot=strategy_df,
                        cmap='YlGnBu', fmt='', cbar=False, ax=axes[idx])
            title = ['Q-Learning Policy', 'Optimal Policy'][idx]
            axes[idx].set_title(title)
            axes[idx].set_xlabel("Dealer's Face-Up Card")
            axes[idx].set_ylabel("Player's Total" if idx % 2 == 0 else "")


def try_policy(policy, ace_policy, countCards, numDecks):
    env = Deck.BlackJackEnv(numDecks)
    rewards = 0.0
    wins = 0
    ties = 0
    moves = {'H': 1, 'S': 0, 'D': 2}
    for _ in range(2000000):
        pl, dl, hasAce, _, reward, rCount, _ = env.start_round()

        while True:
            # If we get dropped on p or g, its a terminal state and we end trial.
            if reward != 0.0:
                rewards += reward
                if reward == 5.0:
                    ties += 1
                if reward > 6.0:
                    wins += 1

                break

            if hasAce:
                if not countCards:
                    action = moves[ace_policy[pl-4][dl-2]]
                else:
                    action = moves[ace_policy[rCount][pl-4][dl-2]]
            else:
                if not countCards:
                    action = moves[policy[pl-4][dl-2]]
                else:
                    action = moves[policy[rCount][pl-4][dl-2]]
            # Take action and get new state

            pl, dl, hasAce, _, reward, rCount, _ = env.next(action)

    return wins/2000000, ties/2000000, (2000000-(wins+ties))/2000000, rewards/2000000


def map_policies_optimal_ace(policies, countCards):
    # Constants
    player_values = list(range(4, 22))
    dealer_cards = list(range(2, 12))
    # Hard Coded Optimal Strategy for comparison with Q-learning:
    # SOURCE: https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
    strat = []

    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'])
    strat.append(['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'])
    strat.append(['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    strat.append(['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'])
    # Insert the hardcoded optimal policy at the beginning of the list
    pols = []

    pols.append(policies)
    pols.append(strat)
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
    axes = axes.flatten()

    for idx, policy in enumerate(pols):
        # Map 'H' to 0, 'S' to 1, and 'D' to 2 for numerical representation
        strategy_numerical = [[0 if cell == 'H' else 1 if cell ==
                               'S' else 2 if cell == 'D' else cell for cell in row] for row in policy]
        strategy_df = pd.DataFrame(
            policy, index=player_values, columns=dealer_cards)
        strategy_df_numerical = pd.DataFrame(
            strategy_numerical, index=player_values, columns=dealer_cards)

        # Plot each heatmap in its subplot
        sns.heatmap(strategy_df_numerical, annot=strategy_df,
                    cmap='YlGnBu', fmt='', cbar=False, ax=axes[idx])
        title = ['Q-Learning Policy', 'Optimal Policy'][idx]
        axes[idx].set_title(title)
        axes[idx].set_xlabel("Dealer's Face-Up Card")
        axes[idx].set_ylabel("Player's Total" if idx % 2 == 0 else "")
