import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Load bot tokens from .env
BOT_TOKENS = {
    "MEXICEGOD_BOT": os.getenv("MEXICEGOD_BOT"),
    "EYESTEB_BOT": os.getenv("EYESTEB_BOT"),
    "EYEOFVAULT_BOT": os.getenv("EYEOFVAULT_BOT"),
    "CHRONOS_BOT": os.getenv("CHRONOS_BOT"),
    "HUNTER_BOT": os.getenv("HUNTER_BOT"),
    # Add all other bot tokens here
}

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL = os.getenv("CHANNEL")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 60))  # default 60 minutes

async def fetch_users(bot_name, bot_token):
    try:
        client = TelegramClient(f"{bot_name}_session", API_ID, API_HASH)
        await client.start(bot_token=bot_token)

        offset = 0
        limit = 100
        all_participants = []

        while True:
            participants = await client(GetParticipantsRequest(
                channel=CHANNEL,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not participants.users:
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)

        print(f"[{bot_name}] Total users fetched: {len(all_participants)}")
        await client.disconnect()
    except Exception as e:
        print(f"[{bot_name}] Error: {e}")

async def main():
    tasks = [fetch_users(name, token) for name, token in BOT_TOKENS.items()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
