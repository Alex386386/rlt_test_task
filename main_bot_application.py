import json
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from data_aggregation import aggregate_payments
from utils import invalid_value

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')


async def start(update: Update, context):
    user_id = update.message.from_user.id
    full_name = update.message.from_user.full_name

    mention = f'<a href="tg://user?id={user_id}">{full_name}</a>'

    await update.message.reply_text(f"Hi {mention}!",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ForceReply(selective=True))


async def handle_message(update: Update, context):
    try:
        data_input = json.loads(update.message.text)
        filled_data = aggregate_payments(data_input)
        await update.message.reply_text(filled_data)
    except json.JSONDecodeError:
        await update.message.reply_text(invalid_value)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
