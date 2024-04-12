from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackContext
from commands.take_request import take_request
from commands.close_request import close_request
from settings.constants import CLOSE_REQ

chat_sessions = {}

async def callback_query_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    action = parts[0]
    identifier = parts[1] if len(parts) > 1 else None
    print(f"Action: {action}, Identifier: {identifier}")

    if action == "chat":
        await handle_chat_action(query, context, identifier)
    elif action == "take" or action == "closereq":
        await handle_request_action(query, context, identifier, update, action)
    elif action == "closechat":
        await close_chat(update, context, identifier)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="Unknown action.")
    await query.message.edit_reply_markup(reply_markup=None)

async def handle_request_action(query, context: CallbackContext, request_id, update, action):
    if action == "take":
        await handle_take_request_action(query, context, request_id, update)
    elif action == "closereq":
        await handle_close_request_action(query, context, request_id, update)
        
async def handle_take_request_action(query, context: CallbackContext, request_id, update):
  user_id = query.from_user.id
  await take_request(update, context, request_id=request_id)
  
async def handle_close_request_action(query, context: CallbackContext, request_id, update):
    user_id = query.from_user.id
    await close_request(update, context, request_id=request_id)

async def handle_chat_action(query, context: CallbackContext, request_id, user_id):
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

async def close_chat(update: Update, context: CallbackContext, request_id: int) -> int:
    query = update.callback_query
    from_id = query.message.chat_id
    if from_id in chat_sessions:
        del chat_sessions[from_id]
        await context.bot.send_message(chat_id=from_id, text="Chat session closed.")

        print("РЕКВЕСТ ID: "+request_id)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Close Request", callback_data=f"closereq_{request_id}")]
        ])
        await context.bot.send_message(chat_id=from_id, text="Would you like to close the request?", reply_markup=reply_markup)
        return CLOSE_REQ