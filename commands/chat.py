from telegram import Update
from telegram.ext import  CallbackContext
chat_sessions = {}

async def callback_query_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    action, user_id = query.data.split("_")

    if action == "chat":
        chat_sessions[query.message.chat_id] = {"client_id": user_id}
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        await context.bot.send_message(chat_id=query.message.chat_id, text="Чат с пользователем начат.")
        await context.bot.send_message(chat_id=user_id, text="Здравствуйте! С вами связывается сотрудник Transtelecom. Ниже вы будете общаться с человеком.")

async def message_handler(update: Update, context: CallbackContext) -> int:
    from_id = update.effective_chat.id
    text = update.message.text

    # ОТ админа К клиенту
    if from_id in chat_sessions:
        client_id = chat_sessions[from_id]["client_id"]
        await context.bot.send_message(chat_id=client_id, text=text)
        return
    
    # ОТ клиента К админу
    for admin_id, session_info in chat_sessions.items():
        if session_info["client_id"] == str(from_id):
            await context.bot.send_message(chat_id=admin_id, text=text)
            return

async def close_chat(update: Update, context: CallbackContext) -> int:
    from_id = update.effective_chat.id
    if from_id in chat_sessions:
        del chat_sessions[from_id]
        await context.bot.send_message(chat_id=from_id, text="Чат завершен.")