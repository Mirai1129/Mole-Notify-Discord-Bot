import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _ROOT_DIR / "config.yaml"
_ENV_PATH = _ROOT_DIR / ".env"
load_dotenv(_ENV_PATH)

with open(_CONFIG_PATH, "r", encoding="utf-8") as stream:
    _config = yaml.safe_load(stream)

ADMIN_IDS = _config.get("admin_ids", [])
GUILD_IDS = _config.get("guild_ids", [])
VOICE_EVENT_CHANNEL_ID = _config["channels"]["voice_event_channel_id"]
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Check bot token if exist before bot running
if not DISCORD_BOT_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not set. Setup .env and fill it in.")

# expose the raw dict too, in case you add more keys later
CONFIG = _config
