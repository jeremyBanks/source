"""All of the persistent state for this program.

Shoved in here instead of using a database because this is just to illustrate the model.
"""
from __future__ import annotations
from typing import Dict, Set, List
from dataclasses import dataclass, field
from enum import Enum
import pickle


@dataclass
class State:
    path: str

    channels_by_id: Dict[int, Channel] = field(default_factory=dict)

    users_by_id: Dict[int, User] = field(default_factory=dict)

    cards_by_slug: Dict[str, Card] = field(default_factory=dict)

    @classmethod
    def load_or_init(Class, path) -> State:
        try:
            return Class.load(path)
        except IOError:
            return Class(path=path)

    @classmethod
    def load(Class, path) -> State:
        with open(path, "rb") as f:
            self = pickle.load(f)
        assert isinstance(self, Class)
        assert self.path == path
        return self

    def save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self, f)


@dataclass
class Channel:
    id: int


@dataclass
class Deck:
    id: int


@dataclass
class User:
    # the internal ID permanently
    id: int
    # the User#1234 tag currently identifying the user
    handle: str

    decks: List[Deck] = field(default_factory=list)


@dataclass(frozen=True)
class Card:
    name: str
    slug: str = field(init=False)
    mana_cost: str
    types: str
    body: str
    colors: Set[str]

    @classmethod
    def from_scryfall_data(Class, data) -> Card:
        return Class(
            name=data["name"],
            mana_cost=data.get("mana_cost", ""),
            types=data.get("type_line", ""),
            body=data.get("oracle_text", ""),
            colors=set(data.get("colors", [])),
        )

    def __post_init__(self):
        return object.__setattr__(self, "slug", self.name.lower().replace(" ", ""))


state = State.load_or_init("state/bin")
