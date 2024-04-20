import random


class BlackJackEnv:

    rCount = 0
    roundStarted = False

    def __str__(self):
        return f"Deck: {self.deck} \nDiscard: {self.discard} \nRunning Count: {self.rCount} \nPlayer Hand: {self.playerHand} \nDealer Hand: {self.dealerHand} \nRound Started: {self.roundStarted}\n hasAce: {self.has_ace()} \n"

    def __init__(self, numDecks, tie_reward=5.0):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * numDecks
        self.rCount = 0  # Running count
        # Also contains cards that are in play (on the table)
        self.discard = []
        self.playerHand = []
        self.dealerHand = []
        self.doubled = False
        self.tie_reward = tie_reward

        self.shuffle()

    def shuffle(self):
        for card in self.discard:
            self.deck.append(card)
        self.discard = []
        self.rCount = 0
        # shuffle 5 times
        for i in range(5):
            random.shuffle(self.deck)

    def hand_value(self, hand):
        value = sum(hand)
        if value > 21 and 11 in hand:
            hand.remove(11)
            hand.append(1)
            value = sum(hand)
        return value

    # might need to change this account for aces that are already overdrawn for value 11

    def has_ace(self):
        if 11 in self.playerHand:
            return 1
        else:
            return 0

    def deal_card(self):
        card = self.deck.pop()
        if card < 7:
            self.rCount += 1
        elif card > 9:
            self.rCount -= 1
        self.discard.append(card)
        return card

    def get_state(self):

        pl = self.hand_value(self.playerHand)
        dl = self.dealerHand[0]
        runningCount = self.get_rCount()
        reward = self.get_reward()
        roundStarted = self.roundStarted

        return (pl, dl, self.has_ace(), roundStarted, reward, runningCount, self.doubled)

    def get_rCount(self):
        if self.rCount > 5:
            return 2
        elif self.rCount < -5:
            return 0
        else:
            return 1

    def get_reward(self):
        if self.roundStarted:
            return 0.0
        else:

            playerValue = self.hand_value(self.playerHand)
            dealerValue = self.hand_value(self.dealerHand)
            if playerValue > 21:
                return -200.0 if self.doubled else -100.0
            if dealerValue > 21:
                return 200.0 if self.doubled else 100.0
            if playerValue > dealerValue:
                return 200.0 if self.doubled else 100.0
            if playerValue < dealerValue:
                return -200.0 if self.doubled else -100.0
            return self.tie_reward

    def end_round(self):

        self.playerHand = []
        self.dealerHand = []

    def start_round(self):
        """
        Starts a new round of blackjack
        Returns: player hand, dealer hand, hasAce, roundStarted, reward, runningCount, hasDoubled
        """
        self.doubled = False
        if len(self.deck) < 15:
            self.shuffle()

        if self.roundStarted:
            print("Round already started")
            return None
        self.roundStarted = True
        self.playerHand = [self.deal_card(), self.deal_card()]
        self.dealerHand = [self.deal_card(), self.deal_card()]
        if self.hand_value(self.playerHand) == 21:
            self.roundStarted = False
            state = self.get_state()
            self.end_round()
            return state
        return self.get_state()

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
            if self.hand_value(self.playerHand) > 21:
                self.roundStarted = False
                state = self.get_state()
                self.end_round()
                return state
            return self.get_state()

        elif action == 0:

            while self.hand_value(self.dealerHand) < 17:
                self.dealerHand.append(self.deal_card())
            self.roundStarted = False
            state = self.get_state()
            self.end_round()
            return state

        elif action == 2:
            self.doubled = True
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

        else:
            return None
