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
from server import app


# ✅ Run Flask server for Render
def run_server():
    port = int(os.environ.get("PORT", 10000))  # Render injects PORT
    app.run(host="0.0.0.0", port=port)


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
    LOGGER("ShrutixMusic").info(
        "Shrutix Music Bot Started Successfully.\n\nDon't forget to visit @ShrutiBots"
    )

    await idle()
    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("Stopping ShrutixMusic Music Bot...")


if __name__ == "__main__":
    # ✅ Start Flask server in background thread
    threading.Thread(target=run_server).start()

    asyncio.get_event_loop().run_until_complete(init())

