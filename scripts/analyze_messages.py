import json
import re
from collections import Counter

with open("/home/hash/.gemini/antigravity-cli/brain/bdf504fd-89e2-43c3-acf6-2fe05a715979/scratch/avalanche_builders_messages.json") as f:
    data = json.load(f)

print("ANALYSIS OF AVALANCHE BUILDER CHATS\n" + "="*50)

all_chats = ["Avalanche Builders 🛠🔺", "Avalanche Builders Hub", "Avalanche Grantees 🔺"]

for chat_name in all_chats:
    chat_info = data.get(chat_name, {})
    msgs = chat_info.get("messages", [])
    
    # Filter out bot msgs
    clean_msgs = []
    for m in msgs:
        sender = (m.get("sender") or "").strip()
        text = (m.get("text") or "").strip()
        if not text or len(text) < 10:
            continue
        if sender.lower() in ["rose", "missrose", "combot"] or "welcomed by Rose" in text or "Welcome to" in text:
            continue
        clean_msgs.append(m)
        
    print(f"\n--- Chat: {chat_name} (Total clean messages: {len(clean_msgs)}) ---")
    
    # Let's inspect all messages and categorize them
    categories = {
        "technical_issues_tooling": [],
        "grants_funding_rfp": [],
        "l1_subnets_acp_avalanche9000": [],
        "product_showcase_pitches": [],
        "community_concerns_worries": [],
        "security_audits": [],
        "events_hackathons": []
    }
    
    for m in clean_msgs:
        t = m["text"]
        t_lower = t.lower()
        s = m["sender"]
        d = m["date"][:10] if m["date"] else ""
        
        assigned = False
        if any(w in t_lower for w in ["fuji", "faucet", "testnet", "rpc", "sdk", "api", "deploy", "contract", "evm", "node", "cli", "glacier"]):
            categories["technical_issues_tooling"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["grant", "funding", "retro", "rfp", "milestone", "payout", "budget", "sponsor"]):
            categories["grants_funding_rfp"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["acp", "acp-77", "9000", "avalanche9000", "l1", "subnet", "teleporter", "icm", "warp", "validator", "staking"]):
            categories["l1_subnets_acp_avalanche9000"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["audit", "security", "pentest", "vulnerability", "hack", "exploit"]):
            categories["security_audits"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["hackathon", "summit", "conference", "event", "basel", "buenos aires", "devcon"]):
            categories["events_hackathons"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["worried", "problem", "difficult", "struggle", "delay", "scam", "frustrat", "issue", "bear", "dead", "liquidity", "volume"]):
            categories["community_concerns_worries"].append((d, s, t))
            assigned = True
        if any(w in t_lower for w in ["we are building", "we're building", "launching", "check out", "announcing", "built on avalanche", "live on"]):
            categories["product_showcase_pitches"].append((d, s, t))
            assigned = True

    for cat, items in categories.items():
        print(f"  * {cat}: {len(items)} items")

