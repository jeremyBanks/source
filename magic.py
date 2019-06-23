from enum import Enum


class Type(Enum):
    basic = "Basic"
    land = "Land"
    artifact = "Artifact"
    creature = "Creature"


class Card:
    name = "Unknown"
    types = set()
