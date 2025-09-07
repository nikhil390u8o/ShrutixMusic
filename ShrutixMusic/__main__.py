import os
import sys
import asyncio
import importlib
import signal
from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutixMusic import LOGGER, nand, userbot
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import sudo
from ShrutixMusic.plugins import ALL_MODULES
from ShrutixMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com

# ─── Web Server ───
async def handle(request):
    return web.Response(text="✅ ShrutixMusic Bot is alive!")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    LOGGER("ShrutixMusic").info(f"🌍 Web server started on port {PORT}")
    return runner

# ─── Bot Init ───
async def init_bot():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        sys.exit(1)

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    await nand.start()

    for all_module in ALL_MODULES:
        importlib.import_module("ShrutixMusic.plugins." + all_module)
    LOGGER("ShrutixMusic.plugins").info("✅ Successfully Imported Modules...")

    await userbot.start()
    await Shruti.start()

    try:
        await Shruti.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutixMusic").error(
            "❌ Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        sys.exit(1)
    except Exception:
        pass

    await Shruti.decorators()
    LOGGER("ShrutixMusic").info("🎵 Shrutix Music Bot Started Successfully!")

    await idle()

    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("🛑 Stopping ShrutixMusic Music Bot...")

# ─── Main ───
async def main():
    # Start web server in background
    await start_web()
    # Start bot
    await init_bot()

def handle_exit(signum, frame):
    print("🛑 Shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    asyncio.run(main())



