# Telethon script to fetch all user IDs from a Telegram channel
# Requires: pip install telethon python-dotenv

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipants
from telethon.tl.types import ChannelParticipantsSearch
from dotenv import load_dotenv
import os

load_dotenv()

# Telegram API credentials (get from https://my.telegram.org)
api_id = int(os.getenv("API_ID"))      # e.g., 123456
api_hash = os.getenv("API_HASH")       # e.g., 'abcdef1234567890abcdef1234567890'
phone = os.getenv("PHONE_NUMBER")      # your number with country code, e.g., '+2348012345678'
channel_username = os.getenv("CHANNEL")  # e.g., 'ICEGODS_ICEMEX'

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone)
    print(f"Fetching users from channel: {channel_username}...")
    offset = 0
    limit = 100
    all_users = []

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

    print(f"Total users fetched: {len(all_users)}")
    with open('channel_users.txt', 'w') as f:
        for user in all_users:
            f.write(f"{user.id} | {user.username}\n")

    print("Saved all user IDs to channel_users.txt")

with client:
    client.loop.run_until_complete(main())
