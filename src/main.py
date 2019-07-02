#!/usr/bin/env python
import asyncio
import json
import os
from pprint import pprint
from typing import FrozenSet
import re
import sys

import aiohttp

"""
https://scryfall.com/docs/api/cards/search
https://discordapp.com/developers/docs/resources/channel#get-channel-messages
https://discordapp.com/developers/docs/topics/gateway
"""


class Card:
    def __init__(self, data):
        self._data = data
        self.slug = re.sub("([^a-z0-9]|s$|^the |^a )+", "", data["name"].lower())

        self.name = data["name"]
        self.cost = data.get("mana_cost") or None
        self.colors = set(data.get("colors") or [])
        self.legal_in = set(
            key for (key, value) in data["legalities"].items() if value == "legal"
        )
        self.type = data["type_line"]
        self.body = data.get("oracle_text") or ""

    def __repr__(self) -> str:
        return "Card" + repr({k: v for (k, v) in self.__dict__.items() if k[:1] != "_"})


async def main():
    with open("scryfall-oracle-bulk.json") as f:
        all_cards = json.load(f)
    legal_cards = [
        Card(card)
        for card in all_cards
        if any(value == "legal" for value in card["legalities"].values())
    ]
    del all_cards
    legal_cards.sort(key=lambda card: card.slug)

    pprint(legal_cards[0:5])

    discord_bot_token = os.environ["DISCORD_TOKEN"]
    test_channel_id = 595358313642721281


if __name__ == "__main__":
    sys.exit(asyncio.get_event_loop().run_until_complete(main(*sys.argv[1:])))
