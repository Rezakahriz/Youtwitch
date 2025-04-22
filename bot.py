from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils import get_live_streamers, read_streamers, add_streamer
import asyncio
import schedule
import time

TOKEN = "7792872499:AAHKDcnRi_3nD9ktKInAfO-0u9MzkoOSME0"
CHANNEL_ID = "https://t.me/Youtwitchtest"

last_message_id = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام ارباب! از دستور /add استفاده کن برای اضافه کردن استریمر.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("فرمت درست: /add USERNAME")
        return
    username = context.args[0]
    if add_streamer(username):
        await update.message.reply_text(f"✅ استریمر {username} اضافه شد.")
    else:
        await update.message.reply_text(f"⚠️ استریمر {username} قبلاً اضافه شده بود.")

async def send_or_edit_message(application):
    global last_message_id
    usernames = read_streamers()
    live = get_live_streamers(usernames)

    if not live:
        text = "🚫 هیچ استریمر فعالی در حال حاضر لایو نیست."
    else:
        text = "🎥 استریمرهای آنلاین:\n"
        for i, (name, views) in enumerate(live, 1):
            text += f"{i}. {name} - {views} بیننده\n"

    if last_message_id:
        try:
            await application.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=last_message_id, text=text)
            return
        except:
            pass

    msg = await application.bot.send_message(chat_id=CHANNEL_ID, text=text)
    last_message_id = msg.message_id

async def scheduler(application):
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))

    schedule.every(6).hours.do(lambda: asyncio.create_task(send_or_edit_message(app)))
    schedule.every(1).hours.do(lambda: asyncio.create_task(send_or_edit_message(app)))

    await asyncio.gather(app.run_polling(), scheduler(app))

if __name__ == "__main__":
    asyncio.run(main())
