import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Fetch interval (optional)
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 60))  # in minutes

# List of bot tokens from .env
bot_tokens = { 
    "MEXICEGOD_BOT": os.getenv("MEXICEGOD_BOT"),
    "EYESTEB_BOT": os.getenv("EYESTEB_BOT"),
    # Add all other bots here like:
    # "ICEGODS_TRACKER": os.getenv("ICEGODS_TRACKER"),
}

async def fetch_users_for_bot(bot_name, bot_token):
    try:
        client = TelegramClient(f"{bot_name}_session", API_ID, API_HASH).start(bot_token=bot_token)
        await client.connect()
        
        # Replace with your channel username
        CHANNEL = os.getenv("CHANNEL")  # e.g., "ICEGODS_ICEMEX"
        
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
        for user in all_participants:
            print(f"[{bot_name}] ID: {user.id}, Name: {user.first_name}, Username: {getattr(user, 'username', '')}")
        await client.disconnect()
    except Exception as e:
        print(f"[{bot_name}] Error: {e}")

async def main():
    tasks = []
    for bot_name, bot_token in bot_tokens.items():
        if bot_token:
            tasks.append(fetch_users_for_bot(bot_name, bot_token))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
