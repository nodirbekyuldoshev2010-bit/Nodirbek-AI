import telebot
from groq import Groq

BOT_TOKEN = "8943785155:AAEoqz9V66h8Ch2dN09kUdUc5MaifrIs2BA"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men AI yordamchiman 🤖 Savolingizni yozing!")

@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi, qayta urinib ko'ring.")

bot.infinity_polling()
