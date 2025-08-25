import os
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio

# Load .env variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL = os.getenv("CHANNEL")

# Optional: Fetch interval in seconds
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 60)) * 60

# List of all bot tokens (for reference, can be used to start multiple clients)
BOT_TOKENS = {key: value for key, value in os.environ.items() if key.endswith("_BOT")}

async def fetch_users():
    async with TelegramClient(PHONE_NUMBER, API_ID, API_HASH) as client:
        while True:
            print(f"Fetching users from channel: {CHANNEL}")
            try:
                participants = await client.get_participants(CHANNEL)
                print(f"Total users fetched: {len(participants)}")
                # Example: Print user IDs
                for user in participants:
                    print(f"ID: {user.id}, Name: {user.first_name} {user.last_name or ''}")
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(fetch_users())
