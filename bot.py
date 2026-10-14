import os
import logging
import telebot
from google import genai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    logging.error("TELEGRAM_BOT_TOKEN atau GEMINI_API_KEY belum diatur di Environment Variables!")
    exit(1)

# Initialize Bot & Gemini Client
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 *Halo! Saya Bot AI Gemini Gratisan 24 Jam.*

"
        "Saya siap membantu menjawab pertanyaan, meriset ide, atau diskusi apapun.
"
        "Kirimkan pesan Anda sekarang!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Tampilkan indikator 'typing...' di Telegram
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Panggil Gemini API (menggunakan model gemini-2.5-flash)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        
        # Kirim balasan ke user
        bot.reply_to(message, response.text)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    logging.info("Bot Telegram Gemini 24 Jam siap berjalan...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
