import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN not set. "
        "Add it to environment variables or to a .env file."
    )

ADMINS = set(
    map(int, os.getenv("ADMINS", "").split())
)  # пример: ADMINS=12345678 98765432
