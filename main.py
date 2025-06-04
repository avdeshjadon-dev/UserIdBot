import telebot
import os

# Bot token from BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8183569140:AAFqlUyLLPSl_i9CFFogdcYLA8Z_L10XFdY"
# Your Telegram user ID for access control
OWNER_ID = XXXXXXXXXX  # <-- Replace this with your real Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)

def log_to_file(file_id, file_type):
    with open("file_ids_log.txt", "a") as f:
        f.write(f"{file_type.upper()} - {file_id}\n")

def is_authorized(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this bot.")
        return False
    return True

@bot.message_handler(content_types=['video'])
def handle_video(message):
    if not is_authorized(message):
        return

    video = message.video
    file_id = video.file_id
    file_size = video.file_size
    duration = video.duration

    log_to_file(file_id, "video")

    reply = (
        f"🎬 *Video Info:*\n"
        f"`{file_id}`\n"
        f"📦 Size: `{file_size}` bytes\n"
        f"⏱ Duration: `{duration}` seconds"
    )
    bot.reply_to(message, reply, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not is_authorized(message):
        return

    photo = message.photo[-1]
    file_id = photo.file_id
    file_size = photo.file_size

    log_to_file(file_id, "photo")

    reply = f"🖼 *Photo File ID:*\n`{file_id}`\n📦 Size: `{file_size}` bytes"
    bot.reply_to(message, reply, parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if not is_authorized(message):
        return

    doc = message.document
    file_id = doc.file_id
    file_name = doc.file_name

    log_to_file(file_id, "document")

    reply = f"📄 *Document:* `{file_name}`\n🆔 File ID: `{file_id}`"
    bot.reply_to(message, reply, parse_mode='Markdown')

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    if not is_authorized(message):
        return

    audio = message.audio
    file_id = audio.file_id
    duration = audio.duration

    log_to_file(file_id, "audio")

    reply = f"🎵 *Audio File ID:*\n`{file_id}`\n⏱ Duration: `{duration}` seconds"
    bot.reply_to(message, reply, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def fallback(message):
    if is_authorized(message):
        bot.reply_to(message, "👋 Send me a video, photo, document, or audio file to get its File ID.")

print("🤖 Bot is running...")
bot.infinity_polling()
