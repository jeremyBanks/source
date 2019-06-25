#!/usr/bin/env python
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace, field
from enum import Enum
from typing import FrozenSet


class Type(Enum):
    """The supertypes that each card can have.
    """

    basic = "Basic"
    land = "Land"


@dataclass(frozen=True)
class Card:
    """A physical card or token, as printed, with no associated state.
    """

    name: str
    types: FrozenSet[Type] = frozenset()
    is_token: bool = False

    def as_token(self):
        """Returns a token copy of this card.
        """

        if self.is_token:
            return self
        else:
            return replace(self, is_token=True)


def main():
    island_card = Card(name="Island", types=frozenset({Type.basic, Type.land}))
    island_token = island_card.as_token()

    print(island_card)
    print(island_token)


if __name__ == "__main__":
    main()
