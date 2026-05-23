import telebot
from groq import Groq
import base64

BOT_TOKEN = "8943785155:AAEoqz9V66h8Ch2dN09kUdUc5MaifrIs2BA"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = "Sen o'zbek tilida javob beradigan AI yordamchisan. Har doim o'zbek tilida, aniq va qisqa javob ber."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men AI yordamchiman 🤖 Matn va rasm yuborishingiz mumkin!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)
        image_base64 = base64.b64encode(downloaded).decode('utf-8')
        caption = message.caption or "Bu rasmda nima bor?"
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "text", "text": caption},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "Rasmni tahlil qilishda xatolik yuz berdi.")

@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi, qayta urinib ko'ring.")

bot.infinity_polling()
