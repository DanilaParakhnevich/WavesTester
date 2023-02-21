import traceback
import telebot
from telebot import types

from manager.WavesManager import WavesManager

bot = telebot.TeleBot("TOKEN_ID")

wavesManager = WavesManager()


@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        get_button = types.KeyboardButton('Получить')
        btc_to_usdt_button = types.KeyboardButton('Обменять BTC на USDT')
        usdt_to_btc_button = types.KeyboardButton('Обменять USDT на BTC')
        markup.row(get_button, btc_to_usdt_button, usdt_to_btc_button)
        bot.send_message(message.chat.id, text='Привет', reply_markup=markup)
    except:
        print(traceback.format_exc())
        bot.reply_to(message, "Bad input")


@bot.message_handler(content_types=['text'])
def get_course(message):
    try:
        if message.text == 'Получить':
            response = wavesManager.get_course_by_asset_names('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS',
                                                              '6XtHjpXbs9RRJP2Sr9GUyVqzACcby9TkThHXnjVC5CDJ')
            bot.reply_to(message, str(response))
        elif message.text == 'Обменять BTC на USDT':
            coef = float(wavesManager.get_course_by_asset_names('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS',
                                                                    '6XtHjpXbs9RRJP2Sr9GUyVqzACcby9TkThHXnjVC5CDJ'))
            bot.send_message(message.chat.id, 'Введите значение валюты для перевода BTC на USDT или напишите символ "q" для выхода')
            bot.register_next_step_handler(message, calculate, coef, 'USDT')
        elif message.text == 'Обменять USDT на BTC':
            coef = float(wavesManager.get_course_by_asset_names('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS',
                                                                    '6XtHjpXbs9RRJP2Sr9GUyVqzACcby9TkThHXnjVC5CDJ'))
            bot.send_message(message.chat.id, 'Введите значение валюты для перевода USDT на BTC или напишите символ "q" для выхода')
            bot.register_next_step_handler(message, calculate, 1 / coef, 'BTC')

    except:
        print(traceback.format_exc())
        bot.reply_to(message, "Bad input")


def calculate(message, coef: float, sym: str) -> None:
    if message.text == 'q':
        return
    try:
        number = float(message.text)

        if number < 0:
            bot.send_message(message.chat.id, 'Неверные данные. Повторите попытку')
            bot.register_next_step_handler(message, calculate, coef, sym)
        else:
            answer = number * coef
            bot.reply_to(message, f'{answer} {sym}')
    except:
        print('bad value: ' + message.text)
        bot.send_message(message.chat.id, 'Неверные данные. Повторите попытку')
        bot.register_next_step_handler(message, calculate, coef, sym)

bot.infinity_polling(none_stop=True, timeout=123)
