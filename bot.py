import telebot
import requests
import json
from config import *

bot = telebot.TeleBot(TOKEN)


class ConvertException(Exception):
    pass


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Хотите начать? Вводиде команду боту в формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидеть список всех доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:

        if len(values) != 3:
            raise ConvertException('Слишком много понаписал.')
        quote, base, amount = values
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertException(bot.reply_to(message, f'Не удалось обработать валюту {quote}'))

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertException(bot.reply_to(message, f'Не удалось обработать валюту {base}'))

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertException(bot.reply_to(message, f'Не удалось обработать колличество {amount}'))

    r = requests.get(f'https://exchange-rates.abstractapi.com/v1/live?api_key=0ee3e75153884fc58c595cc0190b88e6&base={quote_ticker}&target={base_ticker}')

    total_base = json.loads(r.content)
    total_base1 = total_base['exchange_rates'][f'{keys[base]}'] * amount

    text = f'Цена {amount} {quote} в {base} - {total_base1}'
    bot.send_message(message.chat.id, text)


bot.polling()
