import asyncio
import importlib
import threading
import os

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutixMusic import LOGGER, nand, userbot
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import sudo
from ShrutixMusic.plugins import ALL_MODULES
from ShrutixMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
import threading
import os
import threading
from server import app   # import Flask app
from ShrutixMusic import your_bot_start_function  # adjust this

def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Render provides this
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start Flask in background thread
    threading.Thread(target=run_flask).start()
    
    # Start your bot
    your_bot_start_function()





async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await nand.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ShrutixMusic.plugins." + all_module)
    LOGGER("ShrutixMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Shruti.start()
    try:
        await Shruti.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutixMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Shruti.decorators()
    LOGGER("ShrutixMusic").info("Shrutix Music Bot Started Successfully.")
    await idle()
    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("Stopping ShrutixMusic Music Bot...")


import threading, asyncio, server

def start_bot():
    asyncio.run(init())

if __name__ == "__main__":
    # Start bot in background
    threading.Thread(target=start_bot, daemon=True).start()
    # Keep Flask alive on $PORT (Render needs this)
    server.run()




