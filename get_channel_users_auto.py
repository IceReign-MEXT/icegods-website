# Telethon automated channel user fetcher
# Runs every X minutes and updates channel_users.txt

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipants
from telethon.tl.types import ChannelParticipantsSearch
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")
channel_username = os.getenv("CHANNEL")
interval_minutes = int(os.getenv("FETCH_INTERVAL", 60))  # default every 60 minutes

client = TelegramClient('session_name', api_id, api_hash)

async def fetch_users():
    await client.start(phone)
    while True:
        offset = 0
        limit = 100
        all_users = []

        print(f"[+] Fetching users from {channel_username}...")
        while True:
            participants = await client(GetParticipants(
                channel=channel_username,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not participants.users:
                break
            all_users.extend(participants.users)
            offset += len(participants.users)

        with open('channel_users.txt', 'w') as f:
            for user in all_users:
                f.write(f"{user.id} | {user.username}\n")

        print(f"[+] {len(all_users)} users saved to channel_users.txt")
        await asyncio.sleep(interval_minutes * 60)

with client:
    client.loop.run_until_complete(fetch_users())
