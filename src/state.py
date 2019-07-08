"""All of the persistent state for this program.

Shoved in here instead of using a database because this is just to illustrate the model.
"""
from __future__ import annotations
from typing import Dict, Set, List
from dataclasses import dataclass, field, Field
from time import time
from enum import Enum
import jsonpickle
import json
from random import randrange


default = lambda f: field(default_factory=f)
post_init = lambda: field(init=False)


def discord_id() -> int:
    """Generates a 64-bit Discord-like ID whose upper bits represent the current time
    but whose lower bits are random.
    """
    return (int(time() * 1000 - 1420070400000) << 22) + randrange(1 << 22)


def discord_id_time(x: int) -> float:
    """Returns the creation timestamp in a Discord-like ID."""
    return ((x >> 22) + 1420070400000) / 1000


@dataclass
class State:
    path: str

    channels_by_id: Dict[int, Channel] = default(dict)

    users_by_id: Dict[int, User] = default(dict)

    cards_by_slug: Dict[str, Card] = default(dict)

    @classmethod
    def load_or_init(Class, path) -> State:
        try:
            return Class.load(path)
        except (IOError, json.JSONDecodeError):
            return Class(path=path)

    @classmethod
    def load(Class, path) -> State:
        jsonpickle.set_encoder_options("json", indent=0)
        with open(path, "rt") as f:
            self = jsonpickle.decode(f.read(), keys=True)
        assert isinstance(self, Class)
        assert self.path == path
        return self

    def save(self):
        with open(self.path, "wt") as f:
            f.write(jsonpickle.encode(self, keys=True))

    def get_card(self, name) -> Card:
        pass


@dataclass
class Channel:
    id: int
    last_message_id: int = 0


@dataclass
class Deck:
    id: int = default(discord_id)
    card_counts: Dict[Card, int] = default(dict)


@dataclass
class User:
    # the internal ID permanently
    id: int
    # the User#1234 tag currently identifying the user
    handle: str

    decks: List[Deck] = default(list)

    def add_card_to_latest_deck(self):
        pass


@dataclass
class Card:
    name: str
    mana_cost: str
    types: str
    body: str
    colors: Set[str]
    slug: str = post_init()

    def __post_init__(self):
        return object.__setattr__(self, "slug", self.name.lower().replace(" ", ""))

    @classmethod
    def from_scryfall_data(Class, data) -> Card:
        """Creates a Card using some of the data from a Scryfall API JSON card."""
        return Class(
            name=data["name"],
            mana_cost=data.get("mana_cost", ""),
            types=data.get("type_line", ""),
            body=data.get("oracle_text", ""),
            colors=set(data.get("colors", [])),
        )


state = State.load_or_init("state/state.pickle.json")
