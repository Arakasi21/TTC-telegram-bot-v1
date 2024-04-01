from telegram.ext import CallbackContext
from telegram import Update

async def chat_with_user(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /chat <user_id> <сообщение>")
        return

    user_id = context.args[0]
    message = ' '.join(context.args[1:])
    await context.bot.send_message(chat_id=user_id, text=message)