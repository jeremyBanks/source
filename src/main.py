#!/usr/bin/env python
import os
import asyncio

import discord

PLAYING_MAGIC = discord.Game(name="Magic: the Gathering")


class MagicHandsClient(discord.Client):
    channel_id_whitelist = {
        # private mtg #test-1
        305717890357919745,
        # arcbound testing #main
        595358313642721281,
    }

    async def on_ready(self):
        """What do we do first once we're connected to Discord?
        """

        print("Logged on as {0}!".format(self.user))

        await self.change_presence(activity=PLAYING_MAGIC)

    async def on_message(self, message):
        if message.channel.id not in self.channel_id_whitelist:
            # Ignore direct messages and other channels.
            return

        if message.author == self.user:
            # Don't respond to our own messages.
            return

        await message.channel.trigger_typing()
        await asyncio.sleep(1)
        sent = await message.channel.send(
            "{.name}'s `Island.dec` <a:b1nzy:392938283556143104>\n"
            "• 56 Island\n"
            "• 4 Snow-Covered Island".format(message.author)
        )
        print(sent)

    async def on_message_edit(self, message):
        if message.channel.id not in self.channel_id_whitelist:
            # Ignore direct messages and other channels.
            return

        if message.author == self.user:
            # Don't respond to our own messages.
            return

        print("[edited] {0.author}: {0.content}".format(message))


def main():
    client = MagicHandsClient()
    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
