"""All of the persistent state for this program.

Shoved in here instead of using a database because this is just to illustrate the model.
"""
from typing import Dict, Set
from dataclasses import dataclass
import pickle


class State:
    channels_by_id: Dict[int, "Channel"]
    users_by_id: Dict[int, "User"]
    all_cards: Set["Card"]

    # The relative filesystem path the state is being saved to.
    __path: str

    def __init__(self, path):
        self.__path = path

    @classmethod
    def load_or_init(cls, path) -> "State":
        try:
            return cls.load(path)
        except IOError:
            return cls(path=path)

    @classmethod
    def load(cls, path) -> "State":
        with open(path, "rb") as f:
            self = pickle.load(path)
        assert isinstance(self, cls)
        self.__path = path
        return self
    
    def save(self):
        with open(self.__path, "wb") as f:
            pickle.dump(self, f)


class Channel:
    pass


class Deck:
    pass


class User:
    pass


@dataclass(freeze=True)
class Card:
    pass


load = State.load_or_init("state/bin")
