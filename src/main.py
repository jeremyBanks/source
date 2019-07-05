#!/usr/bin/env python3
import asyncio
import json
import os
from pprint import pprint
from typing import FrozenSet
import re
import sys
import pickle
import aiohttp

from state import *


async def main():
    discord_bot_token = os.environ["DISCORD_TOKEN"]
    test_channel_id = 305717890357919745 or 595358313642721281

    print("Loaded", len(state.cards_by_slug), "cards just from state.")

    with open("scryfall-oracle-bulk.json") as f:
        all_cards = json.load(f)
    for card in all_cards:
        if any(value != "not_legal" for value in card["legalities"].values()):
            card = Card.from_scryfall_data(card)
            state.cards_by_slug[card.slug] = card
    print("Loaded", len(state.cards_by_slug), "cards including Scryfall data.")
    state.save()

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
    sys.exit(asyncio.get_event_loop().run_until_complete(main()))
