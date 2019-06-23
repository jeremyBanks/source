from enum import Enum
from random import shuffle

class Board:
    def __init__(self):
        self.hand = []
        self.deck = []
    
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
