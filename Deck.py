import random

# BlackJack Class used as environment for q-learning
# Inspired from the OpenAi blackjack env: https://gymnasium.farama.org/environments/toy_text/blackjack/#version-history


class BlackJackEnv:

    rCount = 0  # Running count of the deck
    roundStarted = False

    def __str__(self):
        return f"Deck: {self.deck} \nDiscard: {self.discard} \nRunning Count: {self.rCount} \nPlayer Hand: {self.playerHand} \nDealer Hand: {self.dealerHand} \nRound Started: {self.roundStarted}\n hasAce: {self.has_ace()} \n"

    # Init takes in number of Decks, and can also specify reward for tie (optional)
    def __init__(self, numDecks, tie_reward=5.0):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * numDecks
        self.rCount = 0  # Running count
        # Also contains cards that are in play (on the table)
        self.discard = []
        self.playerHand = []
        self.dealerHand = []
        self.doubled = False
        self.tie_reward = tie_reward
        self.natural = False

        self.shuffle()

    # Shuffle - put cards in discard back into main deck and shuffle
    def shuffle(self):
        for card in self.discard:
            self.deck.append(card)
        self.discard = []
        self.rCount = 0
        # shuffle 5 times
        for i in range(5):
            random.shuffle(self.deck)

    # helper function gets value of hand and adjusts for aces
    def hand_value(self, hand):
        value = sum(hand)
        if value > 21 and 11 in hand:
            hand.remove(11)
            hand.append(1)
            value = sum(hand)
        return value

    def has_ace(self):
        if 11 in self.playerHand:
            return 1
        else:
            return 0

    # Method to deal a single card - returns the card dealt
    # Also updates running count accordingly
    def deal_card(self):
        card = self.deck.pop()
        if card < 7:
            self.rCount += 1
        elif card > 9:
            self.rCount -= 1
        self.discard.append(card)
        return card

    # Gets the current state of the table
    # Returns player card values, dealerOpen, hasAce(bool), roundStarted(bool),reward,rCount,Doubled(bool)
    def get_state(self):
        pl = self.hand_value(self.playerHand)
        dl = self.dealerHand[0]
        runningCount = self.get_rCount()
        reward = self.get_reward()
        roundStarted = self.roundStarted
        return (pl, dl, self.has_ace(), roundStarted, reward, runningCount, self.doubled)

    # Helper function to create 3 'bins' of running count
    # returns 2 for high, 0 for low, or 1 for neutral
    def get_rCount(self):
        if self.rCount > 4:
            return 2
        elif self.rCount < -4:
            return 0
        else:
            return 1

    # Gets the reward (called at end of round), if round in progress reward is always 0.
    # reward for tie can be adjusted
    def get_reward(self):
        if self.roundStarted:
            return 0.0
        else:

            playerValue = self.hand_value(self.playerHand)
            dealerValue = self.hand_value(self.dealerHand)
            if self.natural and dealerValue != 21:
                return 150.0
            if playerValue > 21:
                return -200.0 if self.doubled else -100.0
            if dealerValue > 21:
                return 200.0 if self.doubled else 100.0
            if playerValue > dealerValue:
                return 200.0 if self.doubled else 100.0
            if playerValue < dealerValue:
                return -200.0 if self.doubled else -100.0
            return self.tie_reward

    # Clears player and dealer hands -- they have already been apended tro discard in deal() function
    def end_round(self):

        self.playerHand = []
        self.dealerHand = []

    # Called to srart a round of blackjack
    def start_round(self):
        """
        Starts a new round of blackjack
        Returns: player hand, dealer hand, hasAce, roundStarted, reward, runningCount, hasDoubled
        """
        self.natural = False
        self.doubled = False
        # Shuffle if deck is too short a start of round
        if len(self.deck) < 12:
            self.shuffle()

        if self.roundStarted:
            print("Round already started")
            return None
        self.roundStarted = True
        self.playerHand = [self.deal_card(), self.deal_card()]
        self.dealerHand = [self.deal_card(), self.deal_card()]
        # If player hit a blackjack, end the round
        if self.hand_value(self.playerHand) == 21:
            self.roundStarted = False
            self.natural = True  # Mark to give extra reward for BlackJack
            state = self.get_state()
            self.end_round()
            return state
        return self.get_state()

    # Called to get the state after a player takes an action
    def next(self, action):
        """
        Takes an action in Blackjack game
        Returns: player hand, dealer hand, hasAce, roundStarted, reward, runningCount, hasDoubled
        """
        if not self.roundStarted:
            print("Round not started")
            return None

        if action == 1:
            self.playerHand.append(self.deal_card())
            # End round if busted, and get state
            if self.hand_value(self.playerHand) > 21:
                self.roundStarted = False
                state = self.get_state()
                self.end_round()
                return state
            # If not busted, don't end round
            return self.get_state()

        elif action == 0:
            # If user stays, dealer draws then round ends
            while self.hand_value(self.dealerHand) < 17:
                self.dealerHand.append(self.deal_card())
            self.roundStarted = False
            state = self.get_state()
            self.end_round()
            return state

        elif action == 2:
            self.doubled = True  # Mark for extra reward/loss for double
            self.playerHand.append(self.deal_card())

            if self.hand_value(self.playerHand) > 21:
                self.roundStarted = False
                state = self.get_state()
                self.end_round()
                return state

            while self.hand_value(self.dealerHand) < 17:
                self.dealerHand.append(self.deal_card())
            self.roundStarted = False
            state = self.get_state()
            self.end_round()
            return state
        # Invalid action
        else:
            return None
