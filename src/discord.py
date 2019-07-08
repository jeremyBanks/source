from __future__ import annotations
from typing import *
import asyncio
import aiohttp
from dataclasses import dataclass
from time import time


class ChannelPollingBot(object):
    api_root = "https://discordapp.com/api/v6"
    poll_interval = 10

    def __init__(self, token: str, channel_id: int):
        self.token: str = token
        self.channel_id: int = channel_id
        self.last_message_id: int = (int(time() * 1000) - 1420070400000 - 360) << 22
        self.on_message_callbacks: List[Callable[[ChannelPollingBot, Dict], []]] = []

    def on_message(self, callback: Callable[[ChannelPollingBot, Dict], []]):
        self.on_message_callbacks.append(callback)

    async def run(self) -> NoReturn:
        while True:
            print("Waiting...")
            await asyncio.sleep(self.poll_interval)
            print("Checking for new messages...")

            async with aiohttp.ClientSession(
                headers={
                    "Authorization": "Bot {}".format(self.token),
                    "User-Agent": "_@jeremy.ca",
                }
            ) as discord_client:
                url = "https://discordapp.com/api/v6/channels/{}/messages".format(
                    self.channel_id
                )
                if self.last_message_id:
                    url += "?after={}".format(self.last_message_id)

                response = await discord_client.get(url)
                content = await response.json()

                print(content)

                for message in content:
                    self.last_message_id = int(message["id"])
                    self.on_message(message)

    async def send(self, content=None, embed=None):
        async with aiohttp.ClientSession(
            headers={
                "Authorization": "Bot {}".format(self.token),
                "User-Agent": "_@jeremy.ca",
            }
        ) as discord_client:
            url = "{}/channels/{}/messages".format(self.api_root, self.channel_id)
            response = await discord_client.post(
                url, json=dict(content=content, embed=embed)
            )
            content = await response.json()
        return content
