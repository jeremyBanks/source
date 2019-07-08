#!/usr/bin/env python3
import asyncio
import json
import os
from pprint import pprint
from typing import FrozenSet
import re
import sys
import aiohttp
import discord

from state import *


async def main():
    discord_bot_token = os.environ["DISCORD_TOKEN"]
    test_channel_id = 595358313642721281 or 305717890357919745

    print("Loaded", len(state.cards_by_slug), "cards just from state.")

    with open("scryfall-oracle-bulk.json") as f:
        all_cards = json.load(f)
    for card in all_cards:
        if any(value != "not_legal" for value in card["legalities"].values()):
            card = Card.from_scryfall_data(card)
            state.cards_by_slug[card.slug] = card
    print("Loaded", len(state.cards_by_slug), "cards including Scryfall data.")
    state.save()

    bot = discord.ChannelPollingBot(token=discord_bot_token, channel_id=test_channel_id)

    @bot.on_message
    async def _(message):
        pprint(message)

    @bot.on_message
    async def _(message):
        message_id = int(message["id"])

        if message["content"].startswith("!deck"):
            pass

        if message["content"].startswith("!card "):
            slug = (message["content"][len("!card ") :]).lower().replace(" ", "")
            card = state.cards_by_slug[slug]
            embed = dict(
                description="**{0.name}**\n*{0.mana_cost} {0.types}*\n{0.body}".format(
                    card
                )
            )

            await bot.send(embed=embed)

    await bot.send(content="Hello, world!")

    await bot.run()


if __name__ == "__main__":
    sys.exit(asyncio.get_event_loop().run_until_complete(main()))
