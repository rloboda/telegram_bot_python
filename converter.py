import telebot
from currency_converter import CurrencyConverter
from telebot import types


TOKEN=open("TOKEN.txt", "r").read()
amount=0

bot =telebot.TeleBot(TOKEN)
currency= CurrencyConverter()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "write sum")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try :
        amount=int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Incorrect value")
        bot.register_next_step_handler(message, summa)
        return

    if amount>0:
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("EUR/PLN", callback_data="eur/pln")
        btn4 = types.InlineKeyboardButton("Write value", callback_data="else")

        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id, "Choose", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "value must be bigger than 0 ")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func= lambda call : True)
def callback(call):
    if call.data != "else":
        value=call.data.upper().split("/")
        res=currency.convert(amount, value[0], value[1])
        bot.send_message(call.message.chat.id, f"Result : {round(res,2)}. Write another sum")
        bot.register_next_step_handler(call.message, summa)
        print(currency.currencies)
    else:
        bot.send_message(call.message.chat.id, "write your value")
        bot.register_next_step_handler(call.message, my_converter)


def my_converter(message):
    try:
        value = message.text.upper().split("/")
        res = currency.convert(amount, value[0], value[1])
        bot.send_message(message.chat.id, f"Result : {round(res, 2)}. Write another sum")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, " Something is wrong. Write one more time")
        bot.register_next_step_handler(message, summa)



bot.polling(none_stop=True)