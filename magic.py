from enum import Enum
from random import shuffle


class Board:
    def __init__(self):
        self.hand = []
        self.deck = []
    
    def shuffle_into_deck(self, cards):
        """Adds cards from outside of the game to the deck, and shuffles it."""
        self.deck.extend(cards)
        self.shuffle()
    
    def shuffle(self):
        """Shuffles the deck."""
        shuffle(self.deck)

    def reset(self):
        """Shuffles all cards into the deck, then draws 7 cards."""
        self.shuffle_into_deck(self.hand)
        self.hand.clear()
        for _ in range(7):
            self.draw()

    def draw(self):
        """Draws a card from the deck to the hand."""
        self.hand.append(self.deck.pop())


class Type(Enum):
    basic = "Basic"
    land = "Land"
    artifact = "Artifact"
    creature = "Creature"


class Card:
    name = "Unknown"
    types = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return type(self).__name__
