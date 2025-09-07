import asyncio
import importlib
import signal
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutixMusic import LOGGER, nand, userbot
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import sudo
from ShrutixMusic.plugins import ALL_MODULES
from ShrutixMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

WEBHOOK_URL = "https://shrutixmusichu.onrender.com"
PORT = "8000"


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
        importlib.import_module("ShrutixMusic.plugins" + all_module)
    LOGGER("ShrutixMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Shruti.start()
    try:
        await Shruti.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutixMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Shruti.decorators()
    LOGGER("ShrutixMusic").info(
    "\x53\x68\x72\x75\x74\x69\x78\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\n\n\x44\x6f\x6e'\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x53\x68\x72\x75\x74\x69\x42\x6f\x74\x73"
)
    await idle()
    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("Stopping ShrutixMusic Music Bot...")


flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            update_json = request.get_json(force=True)
            update = Update.de_json(update_json, application.bot)
            # Run the processing in the async loop
            asyncio.run_coroutine_threadsafe(application.process_update(update), async_loop)
            return 'OK', 200
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            return 'Error', 500
    return 'OK', 200

# Global async loop
async_loop = None

async def handle(request):
    return web.Response(text="✅ Bot is alive!")

async def webhook_handler(request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        application.update_queue.put_nowait(update)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return web.Response(text="OK")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    app.router.add_post("/webhook", webhook_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"🌍 Web server started on port {PORT}")
    return runner

def run_web():
    asyncio.run(start_web())

# ─── Main ────────────────────────────────
async def main():
    load_data()
    logger.info("🤖 Bot starting in webhook mode...")

    # Start aiohttp server
    await start_web()

    # Initialize and start application
    await application.initialize()
    await application.start()

    # Set webhook
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com
    if not WEBHOOK_URL:
        logger.error("❌ WEBHOOK_URL not set in environment variables")
        sys.exit(1)

    await application.bot.set_webhook(WEBHOOK_URL + "/webhook")
    logger.info(f"🤖 Webhook set to {WEBHOOK_URL}/webhook")

    # Keep running forever
    await asyncio.Event().wait()


def handle_exit(signum, frame):
    print("🛑 Shutting down...")
    sys.exit(0)
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    asyncio.run(main())


