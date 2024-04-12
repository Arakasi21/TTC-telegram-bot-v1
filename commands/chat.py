from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackContext
from commands.take_request import take_request
from commands.close_request import close_request
from settings.constants import CLOSE_REQ

chat_sessions = {}
print(chat_sessions)

async def callback_query_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    data_parts = query.data.split("_", 2)
    action = data_parts[0]
    request_id = data_parts[1]
    client_id = None
    if len(data_parts) >= 3:
        client_id = data_parts[2]
    print(f"Action: {action}, Request ID: {request_id}, Client ID: {client_id}")

    if action == "chat":
        await handle_chat_action(query, context, client_id, request_id)
    elif action == "take":
        await handle_take_request_action(query, context, request_id, update)
    elif action == "closereq":
        await handle_close_request_action(query, context, request_id, update)
    elif action == "closechat":
        await close_chat(update, context, client_id, request_id)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="Unknown action.")
    await query.message.edit_reply_markup(reply_markup=None)

async def handle_take_request_action(query, context: CallbackContext, request_id, update):
  user_id = query.from_user.id
  await take_request(update, context, request_id=request_id)
  
async def handle_close_request_action(query, context: CallbackContext, request_id, update):
    user_id = query.from_user.id
    await close_request(update, context, request_id=request_id)

async def handle_chat_action(query, context: CallbackContext, user_id, request_id):
    chat_sessions[query.message.chat_id] = {"client_id": user_id}
    await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Close Chat", callback_data=f"closechat_{request_id}_{user_id}")]
    ])
    await context.bot.send_message(chat_id=query.message.chat_id, text=f"Чат с пользователем {user_id} начат.", reply_markup=reply_markup)
    await context.bot.send_message(chat_id=user_id, text="Здравствуйте! С вами связывается сотрудник Transtelecom. Ниже вы будете общаться с человеком.")

async def message_handler(query, context: CallbackContext, update) -> int:
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

async def close_chat(update: Update, context: CallbackContext, client_id: int, request_id: int) -> int:
    query = update.callback_query
    from_id = query.message.chat_id
    if from_id in chat_sessions:
        del chat_sessions[from_id]

        await context.bot.send_message(chat_id=from_id, text="Chat session closed.")

        print("РЕКВЕСТ ID: "+ request_id)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Close Request", callback_data=f"closereq_{request_id}")]
        ])
        await context.bot.send_message(chat_id=from_id, text="Would you like to close the request?", reply_markup=reply_markup)
        return CLOSE_REQ