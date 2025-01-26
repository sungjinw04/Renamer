from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import asyncio
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1002425816622

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8090).start()     
        print(f"{me.first_name} Is Started.....✨️")
        for id in Config.ADMIN:
            try:
                await self.send_message(Config.LOG_CHANNEL, f"**{me.first_name}  Is Started.....✨️**")                                
            except:
                pass
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")                                
            except:
                print("Please Make This Bot Admin In Your Log Channel")

async def main():
    bot = Bot()
    await bot.start()
    await asyncio.Event().wait()  # Keep the bot running

if __name__ == "__main__":
    try:
        # Check if an event loop is already running
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If the loop is running, schedule `main()` instead
            loop.create_task(main())
        else:
            # If no loop is running, use `asyncio.run`
            asyncio.run(main())
    except RuntimeError:
        # Fallback for environments with issues
        asyncio.run(main())

