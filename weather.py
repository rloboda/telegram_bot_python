import telebot
import requests
import json
from datetime import datetime

TOKEN=open("TOKEN.txt", "r").read()
API="0b2af477e388a25ac5cc6ebe0ac57ca0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(['start'])
def start(message):
    bot.send_message(message.chat.id, "write city")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city=message.text.strip().lower()
    res=requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)

        date=datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')

        bot.reply_to(message,f"Temperature : {data['main']['temp']}\n"
                             f"Wind speed : {data['wind']['speed']}\n"
                             f"Weather : {data['weather'][0]['main']}\n"
                             f"Details : {data['weather'][0]['description']}\n"
                             f"sunrise : {date}\n")
    else:
        bot.reply_to(message, 'City name is not correct ')





bot.polling(none_stop=True)