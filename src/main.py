#!/usr/bin/env python
import asyncio
import json
import os
from pprint import pprint
from typing import FrozenSet
import re
import sys
import pickle

import aiohttp

"""
https://scryfall.com/docs/api/cards/search
https://discordapp.com/developers/docs/resources/channel#get-channel-messages
https://discordapp.com/developers/docs/topics/gateway
"""


class State:
    filename = "state"

    def __init__(self):
        self.last_message_id = 0

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self, f)


try:
    with open(State.filename, "rb") as f:
        state = pickle.load(f)
except IOError:
    state = State()


class Card:
    def __init__(self, data):
        self._data = data
        self.slug = slugify(data["name"])

        self.name = data["name"]
        self.cost = data.get("mana_cost") or None
        self.colors = set(data.get("colors") or [])
        self.legal_in = set(
            key for (key, value) in data["legalities"].items()  # if value != "banned"
        )
        self.type = data["type_line"]
        self.body = data.get("oracle_text") or ""

    def __repr__(self) -> str:
        return "Card" + repr({k: v for (k, v) in self.__dict__.items() if k[:1] != "_"})


def slugify(s) -> str:
    return re.sub("([^a-z0-9]|s+$|^the |^a )+", "", s.lower())


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
    cards_by_slug = {card.slug: card for card in legal_cards}
    print("got", len(cards_by_slug), "cards")

    discord_bot_token = os.environ["DISCORD_TOKEN"]
    test_channel_id = 305717890357919745 or 595358313642721281

    async with aiohttp.ClientSession(
        headers={
            "Authorization": "Bot {}".format(discord_bot_token),
            "User-Agent": "_@jeremy.ca",
        }
    ) as discord_client:
        response = await discord_client.get(
            "https://discordapp.com/api/v6/channels/{}/messages?after={}".format(
                test_channel_id, state.last_message_id
            )
        )
        data = await response.json()
        for message in data:
            message_id = int(message["id"])
            if message_id > state.last_message_id:
                state.last_message_id = message_id

            if message["content"].startswith("!card "):
                slug = slugify(message["content"][len("!card ") :])
                card = cards_by_slug[slug]

                print(
                    await (
                        await discord_client.post(
                            "https://discordapp.com/api/v6/channels/{}/messages".format(
                                test_channel_id
                            ),
                            json=dict(
                                embed=dict(
                                    description="**{0.name}**\n*{0.cost} {0.type}*\n{0.body}".format(
                                        card
                                    )
                                )
                            ),
                        )
                    ).json()
                )

        state.save()


if __name__ == "__main__":
    sys.exit(asyncio.get_event_loop().run_until_complete(main(*sys.argv[1:])))
