import traceback
import telebot
from telebot import types
from waves_python.account.address import Address
from waves_python.api.node import Node
from waves_python.api.profile import Profile

from manager.WavesManager import WavesManager

bot = telebot.TeleBot("6297640805:AAHEihL5tfC5j3a9u4MBKKiOt7XYxUDNJiE")

wavesManager = WavesManager()

UDST_CONST = 'USDT'
WBTC_CONST = 'BTC'


@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, text='Все функции предоставлены на клавиатуре', reply_markup=getDefaultKeyboardKeyboardMarkup())
    except:
        print(traceback.format_exc())
        bot.reply_to(message, "Bad input")


@bot.message_handler(content_types=['text'])
def get_course(message):
    try:
        if message.text == 'Получить':
            response = wavesManager.get_course_by_asset_names(WBTC_CONST, UDST_CONST)
            bot.reply_to(message, f'1 BTC = {response} UDST')
        elif message.text == 'Обменять BTC на USDT':
            coef = float(wavesManager.get_course_by_asset_names(WBTC_CONST, UDST_CONST))
            bot.send_message(message.chat.id, 'Введите значение валюты для перевода BTC на USDT или напишите символ "q" для выхода')
            bot.register_next_step_handler(message, calculate, coef, 'BTC', 'USDT')
        elif message.text == 'Обменять USDT на BTC':
            coef = float(wavesManager.get_course_by_asset_names(WBTC_CONST, UDST_CONST))
            bot.send_message(message.chat.id, 'Введите значение валюты для перевода USDT на BTC или напишите символ "q" для выхода')
            bot.register_next_step_handler(message, calculate, 1 / coef, 'USDT', 'BTC')

    except:
        print(traceback.format_exc())
        bot.reply_to(message, "Bad input")


def calculate(message, coef: float, sym_from: str, sym: str) -> None:
    if message.text == 'q':
        return
    try:
        number = float(message.text)

        if number < 0:
            bot.send_message(message.chat.id, 'Неверные данные. Повторите попытку')
            bot.register_next_step_handler(message, calculate, coef, sym_from, sym)
        else:
            confirmation(message, number, coef, sym_from, sym)
    except:
        print('bad value: ' + message.text)
        bot.send_message(message.chat.id, 'Неверные данные. Повторите попытку')
        bot.register_next_step_handler(message, calculate, coef, sym_from, sym)


def confirmation(message, number: float, coef: float, sym_from: str, sym: str) -> None:
    markup = types.ReplyKeyboardMarkup()
    yes_button = types.KeyboardButton('Да')
    no_button = types.KeyboardButton('Нет')
    markup.row(yes_button, no_button)
    bot.send_message(message.chat.id, text=f'Переведите {number} {sym_from} на счёт: 3PQggfuKn4NMvujjBJijCwm7PpmseC1Q3hi')
    bot.send_message(message.chat.id, text='Вы уже перевели деньги на указанный счёт?', reply_markup=markup)

    bot.register_next_step_handler(message, print_after_confirmation, coef, number, sym, get_balance())


def print_after_confirmation(message, coef: float, number: float, sym: str, balance: float) -> None:
    if message.text == 'Да':

        if get_balance() - balance >= number:
            bot.send_message(message.chat.id, f'Результат обмена: {coef * float} {sym}', reply_markup=getDefaultKeyboardKeyboardMarkup())
        else:
            bot.send_message(message.chat.id, 'Сумма не была переведена на счет. Отмена обмена', reply_markup=getDefaultKeyboardKeyboardMarkup())

    else:
        bot.send_message(message.chat.id, 'Отмена обмена', reply_markup=getDefaultKeyboardKeyboardMarkup())


def get_balance() -> float:
    address = Address(base58_str="3PQggfuKn4NMvujjBJijCwm7PpmseC1Q3hi")
    node = Node(Profile.MAINNET)
    return node.get_address_balance(address)


def getDefaultKeyboardKeyboardMarkup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup()
    get_button = types.KeyboardButton('Получить')
    btc_to_usdt_button = types.KeyboardButton('Обменять BTC на USDT')
    usdt_to_btc_button = types.KeyboardButton('Обменять USDT на BTC')
    markup.row(get_button, btc_to_usdt_button, usdt_to_btc_button)
    return markup


bot.infinity_polling(none_stop=True, timeout=123)
