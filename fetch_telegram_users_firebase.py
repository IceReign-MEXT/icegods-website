import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from telethon import TelegramClient

# Load environment variables from .env
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL = os.getenv("CHANNEL")  # e.g., "ICEGODS_ICEMEX"
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Optional for bot-based access

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Place your Firebase JSON here
firebase_admin.initialize_app(cred)
db = firestore.client()

async def fetch_users():
    async with TelegramClient('session', API_ID, API_HASH).start(bot_token=BOT_TOKEN) as client:
        async for user in client.iter_participants(CHANNEL):
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "username": user.username,
                "is_bot": user.bot,
                "app_version": getattr(user, "app_version", "unknown")
            }
            print(f"[{user.username}] ID: {user.id}, App Version: {user_data['app_version']}")
            # Save to Firebase
            db.collection("telegram_users").document(str(user.id)).set(user_data)

asyncio.run(fetch_users())
