from abc import ABC, abstractmethod
from dataclasses import dataclass, replace, field
from enum import Enum
from typing import FrozenSet, Sequence


class Type(Enum):
    """The supertypes that each card can have.
    """

    basic = "Basic"
    land = "Land"
    creature = "Creature"
    artifact = "Artifact"
    legendary = "Legendary"
    instant = "Instant"
    sorcery = "Sorcery"
    token = "Token"


basic = Type.basic
land = Type.land
creature = Type.creature
artifact = Type.artifact
legendary = Type.legendary
instant = Type.instant
sorcery = Type.sorcery
instant = Type.instant
token = Type.token

class Ability(ABC):
    NotImplemented

class ManaAbility(Ability):
    NotImplemented


@dataclass(frozen=True)
class Card:
    """A "physical" card or token, as printed, with no associated state.
    """

    name: str
    types: FrozenSet[Type] = frozenset()
    abilities: Sequence[Ability] = ()
    power: int = 0
    toughness: int = 0
    is_token: bool = False

    def as_token(self):
        """Returns a token copy of this card.
        """

        if self.is_token:
            return self
        else:
            return replace(self, is_token=True, types=self.types | {token})
