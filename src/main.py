#!/usr/bin/env python3
import asyncio
import json
import os
from pprint import pprint
from typing import FrozenSet
import re
import sys
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

    channel = state.channels_by_id.setdefault(
        test_channel_id, Channel(id=test_channel_id)
    )

    async with aiohttp.ClientSession(
        headers={
            "Authorization": "Bot {}".format(discord_bot_token),
            "User-Agent": "_@jeremy.ca",
        }
    ) as discord_client:
        if sys.argv[1:2] == ["bot"]:
            while True:
                url = "https://discordapp.com/api/v6/channels/{}/messages".format(
                    channel.id
                )
                if channel.last_message_id:
                    url += "?after={}".format(channel.last_message_id)
                response = await discord_client.get(url)
                data = await response.json()
                print("got", len(data), "messages after", channel.last_message_id)
                for message in data:
                    message_id = int(message["id"])
                    if message_id > channel.last_message_id:
                        channel.last_message_id = message_id

                    if message["content"].startswith("!deck"):
                        pass

                    if message["content"].startswith("!card "):
                        slug = (
                            (message["content"][len("!card ") :])
                            .lower()
                            .replace(" ", "")
                        )
                        card = state.cards_by_slug[slug]

                        print(
                            await (
                                await discord_client.post(
                                    "https://discordapp.com/api/v6/channels/{}/messages".format(
                                        channel.id
                                    ),
                                    json=dict(
                                        embed=dict(
                                            description="**{0.name}**\n*{0.mana_cost} {0.types}*\n{0.body}".format(
                                                card
                                            )
                                        )
                                    ),
                                )
                            ).json()
                        )

                await asyncio.sleep(5)
        else:
            raise "invalid comman d"

        state.save()


if __name__ == "__main__":
    sys.exit(asyncio.get_event_loop().run_until_complete(main()))
