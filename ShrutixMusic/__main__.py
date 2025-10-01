import asyncio
import importlib

from pyrogram import idle
from pyrogram.errors import FloodWait
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutixMusic import LOGGER, nand, userbot
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import sudo
from ShrutixMusic.plugins import ALL_MODULES
from ShrutixMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


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

    # Load banned users into memory
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("ShrutixMusic").warning(f"Error loading banned users: {e}")

    # --- Handle FloodWait during start ---
    try:
        await nand.start()
    except FloodWait as e:
        LOGGER("ShrutixMusic").warning(f"FloodWait: sleeping {e.value} seconds before retrying...")
        await asyncio.sleep(e.value)
        await nand.start()

    # Import plugins
    for all_module in ALL_MODULES:
        importlib.import_module("ShrutixMusic.plugins" + all_module)
    LOGGER("ShrutixMusic.plugins").info("Successfully Imported Modules...")

    # Start userbot
    try:
        await userbot.start()
    except FloodWait as e:
        LOGGER("ShrutixMusic").warning(f"FloodWait on userbot: sleeping {e.value} seconds...")
        await asyncio.sleep(e.value)
        await userbot.start()

    # Start pytgcalls
    try:
        await Shruti.start()
    except FloodWait as e:
        LOGGER("ShrutixMusic").warning(f"FloodWait on Shruti: sleeping {e.value} seconds...")
        await asyncio.sleep(e.value)
        await Shruti.start()

    try:
        await Shruti.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutixMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except Exception as e:
        LOGGER("ShrutixMusic").warning(f"Stream error ignored: {e}")

    await Shruti.decorators()
    LOGGER("ShrutixMusic").info(
        "Shrutix Music Bot Started Successfully.\n\nDon't forget to visit @ShrutiBots"
    )

    await idle()

    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("Stopping ShrutixMusic Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
