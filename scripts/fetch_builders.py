import asyncio
import os
import json
from datetime import datetime, timezone
from telethon import TelegramClient

CONFIG_DIR = os.path.expanduser("~/.config/telethon")
SESSION_FILE = os.path.join(CONFIG_DIR, "tg_session")
with open(os.path.join(CONFIG_DIR, "config.json")) as f:
    cfg = json.load(f)

TARGET_CHATS = [
    {"id": -1001365896273, "name": "Avalanche Builders 🛠🔺"},
    {"id": -1001871806091, "name": "Avalanche Builders Hub"},
    {"id": -1002453822530, "name": "Avalanche Grantees 🔺"}
]

async def main():
    client = TelegramClient(SESSION_FILE, cfg["api_id"], cfg["api_hash"])
    await client.connect()
    
    results = {}
    
    for chat in TARGET_CHATS:
        chat_id = chat["id"]
        chat_name = chat["name"]
        print(f"Fetching messages for {chat_name} ({chat_id})...")
        messages = []
        try:
            entity = await client.get_entity(chat_id)
            async for msg in client.iter_messages(entity, limit=400):
                if not msg.text and not msg.media:
                    continue
                sender_name = "Unknown"
                username = ""
                if msg.sender:
                    sender_name = f"{getattr(msg.sender, 'first_name', '') or ''} {getattr(msg.sender, 'last_name', '') or ''}".strip()
                    username = getattr(msg.sender, 'username', '') or ''
                
                messages.append({
                    "id": msg.id,
                    "date": msg.date.isoformat() if msg.date else None,
                    "sender": sender_name,
                    "username": username,
                    "reply_to": msg.reply_to_msg_id if msg.reply_to else None,
                    "text": msg.text or f"[{msg.media.__class__.__name__}]"
                })
            results[chat_name] = {
                "id": chat_id,
                "count": len(messages),
                "messages": messages
            }
            print(f"Retrieved {len(messages)} messages for {chat_name}")
        except Exception as e:
            print(f"Error fetching {chat_name}: {e}")
            results[chat_name] = {"error": str(e)}

    out_file = "/home/hash/.gemini/antigravity-cli/brain/bdf504fd-89e2-43c3-acf6-2fe05a715979/scratch/avalanche_builders_messages.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved results to {out_file}")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
