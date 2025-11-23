import logging
import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import InputMediaPhoto
from datetime import datetime

# Bot Token
BOT_TOKEN = "8262872880:AAEHzUOMCx_aTxPGOWh9wUC_a2VTwSJsU70"
ADMIN_USERNAME = "SUNNY_BRO1"

# User data file
USER_DATA_FILE = "users.json"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"users": []}

# Save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=4)

# Add user to database
def add_user(user_id, username, first_name):
    user_data = load_user_data()
    user_exists = any(user['user_id'] == user_id for user in user_data['users'])
    
    if not user_exists:
        user_data['users'].append({
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'joined_at': datetime.now().isoformat()
        })
        save_user_data(user_data)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    
    photo_url = "https://i.ibb.co/S7tNCrMr/20251122-131336.jpg"
    keyboard = [
        [
            InlineKeyboardButton("1WIN", callback_data="1win"),
            InlineKeyboardButton("MELBET", callback_data="melbet"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_photo(
            photo=photo_url,
            caption="",
            reply_markup=reply_markup
        )
    else:
        await update.callback_query.message.reply_photo(
            photo=photo_url,
            caption="",
            reply_markup=reply_markup
        )

# Button click handler
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "1win":
        photo_url = "https://i.ibb.co/gLYrFH3H/20251121-053322.png"
        caption = """🌐 Account Setup Required
✦ Start by creating a fresh account using the link below.
✦ While signing up, don't forget to apply the promo code: BLACK110
❗ If the link redirects to your old account, simply log out and open the registration link again to continue.
● After completing your registration, press the ✅ Done ✅ button to move forward."""
        
        keyboard = [
            [
                InlineKeyboardButton("Register Now✨", web_app=WebAppInfo(url="https://1wsbeh.com/casino/list?open=register&p=mth6")),
                InlineKeyboardButton("Done 🎇", callback_data="1win_done")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_media(
            media=InputMediaPhoto(media=photo_url, caption=caption)
        )
        await query.edit_message_reply_markup(reply_markup=reply_markup)

    elif query.data == "melbet":
        photo_url = "https://i.ibb.co/p695QGjD/20251122-130201.jpg"
        caption = """🌐 Account Setup Required
✦ Start by creating a fresh account using the link below.
✦ While signing up, don't forget to apply the promo code: BLACK220
❗ If the link redirects to your old account, simply log out and open the registration link again to continue.
● After completing your registration, press the ✅ Done ✅ button to move forward."""
        
        keyboard = [
            [
                InlineKeyboardButton("Register Now✨", web_app=WebAppInfo(url="https://melbet-10591.today/en/registration?bonus=SPORT")),
                InlineKeyboardButton("Done 🎇", callback_data="melbet_done")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_media(
            media=InputMediaPhoto(media=photo_url, caption=caption)
        )
        await query.edit_message_reply_markup(reply_markup=reply_markup)

    elif query.data in ["1win_done", "melbet_done"]:
        photo_url = "https://i.ibb.co/qYrP3TkN/IMG-20251121-052819-201.jpg"
        caption = "Great! Now you can access our features"
        
        keyboard = [
            [
                InlineKeyboardButton("Aviator Hack", web_app=WebAppInfo(url="https://aviatorvipsignal.ct.ws/")),
                InlineKeyboardButton("Mines Hack", web_app=WebAppInfo(url="https://minesgame1win.xo.je/")),
            ],
            [
                InlineKeyboardButton("Apple Hack", web_app=WebAppInfo(url="https://paidapple23vip.kesug.com/")),
                InlineKeyboardButton("Thimbles King", web_app=WebAppInfo(url="https://kingthimbles.ct.ws/"))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_media(
            media=InputMediaPhoto(media=photo_url, caption=caption)
        )
        await query.edit_message_reply_markup(reply_markup=reply_markup)

# Admin command handler - Show admin panel
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    
    admin_panel_text = """🛠️ ADMIN PANEL

🔧 Available Commands:
• /broadcast - Send message to all users
• /users - Show user count
• /stats - Show statistics"""
    
    await update.message.reply_text(admin_panel_text)

# Show user count
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    
    user_data = load_user_data()
    total_users = len(user_data['users'])
    
    await update.message.reply_text(f"👥 Total Users: {total_users}")

# Show statistics
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    
    user_data = load_user_data()
    total_users = len(user_data['users'])
    
    # Calculate today's new users
    today = datetime.now().date()
    today_users = 0
    for user in user_data['users']:
        user_date = datetime.fromisoformat(user['joined_at']).date()
        if user_date == today:
            today_users += 1
    
    stats_text = f"""📊 Bot Statistics

👥 Total Users: {total_users}
📈 New Users Today: {today_users}"""

    await update.message.reply_text(stats_text)

# Broadcast command handler - Step 1: Ask for message
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    
    # Set broadcast mode and ask for message
    context.user_data['broadcast_mode'] = True
    await update.message.reply_text(
        "📢 **Send the message you want to broadcast to all users:**\n\n"
        "You can send text, photo, video, or document."
    )

# Handle all messages for broadcast
async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    # Check if user is admin and in broadcast mode
    if user.username != ADMIN_USERNAME or not context.user_data.get('broadcast_mode'):
        return
    
    # Get the message details
    message = update.message
    user_data = load_user_data()
    total_users = len(user_data['users'])
    successful = 0
    failed = 0
    
    # Send progress message
    progress_msg = await update.message.reply_text(f"📤 Sending broadcast to {total_users} users...")
    
    # Send to all users based on message type
    for user_obj in user_data['users']:
        try:
            if message.text:
                # Text message
                await context.bot.send_message(
                    chat_id=user_obj['user_id'],
                    text=message.text
                )
            elif message.photo:
                # Photo with caption
                photo = message.photo[-1]  # Highest resolution
                caption = message.caption if message.caption else ""
                await context.bot.send_photo(
                    chat_id=user_obj['user_id'],
                    photo=photo.file_id,
                    caption=caption
                )
            elif message.video:
                # Video with caption
                caption = message.caption if message.caption else ""
                await context.bot.send_video(
                    chat_id=user_obj['user_id'],
                    video=message.video.file_id,
                    caption=caption
                )
            elif message.document:
                # Document with caption
                caption = message.caption if message.caption else ""
                await context.bot.send_document(
                    chat_id=user_obj['user_id'],
                    document=message.document.file_id,
                    caption=caption
                )
            successful += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send broadcast to {user_obj['user_id']}: {e}")
    
    # Clear broadcast mode
    context.user_data.pop('broadcast_mode', None)
    
    # Send result
    result_text = f"""✅ Broadcast Completed!

✅ Successful: {successful}
❌ Failed: {failed}
📊 Total: {total_users}"""
    
    await progress_msg.edit_text(result_text)

# Cancel broadcast if needed
async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    if user.username != ADMIN_USERNAME:
        return
    
    if context.user_data.get('broadcast_mode'):
        context.user_data.pop('broadcast_mode', None)
        await update.message.reply_text("❌ Broadcast cancelled.")

def main() -> None:
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CommandHandler("users", users))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("cancel", cancel_broadcast))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Message handler for broadcast (must be after command handlers)
    # Use filters.ATTACHMENT for documents instead of filters.DOCUMENT
    application.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.ATTACHMENT, 
        handle_broadcast_message
    ))

    # Start bot
    application.run_polling()
    print("Bot is running...")

if __name__ == "__main__":
    main()