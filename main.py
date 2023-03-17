import telebot
from config import TOKEN, names
from extensios import APIException, Converter


bot = telebot.TeleBot(TOKEN)

# Обработчик команд '/start' и '/help'
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    # Текст, который будет отправлен пользователю в ответ на команды '/start' и '/help'
    sss = 'Конвертер валют. Введите:\n\n<aaa> <bbb> <ccc>\n\n<aaa>-имя валюты цену которой необходимо узнать\n' \
          '<bbb>-имя валюты в которой надо узнать цену первой валюты \n<ccc>-количество первой валюты\n\n' \
          'Пример: рубль доллар 10\n\n/values - список доступных валют'
    bot.reply_to(message, sss)

# Обработчик команды '/values'
@bot.message_handler(commands=['values'])
def handle_values(message):
    # Текст, который будет отправлен пользователю в ответ на команду '/values'
    sss = 'Доступные валюты:\n' + '\n'.join(names.keys())
    bot.reply_to(message, sss)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Разбиваем текст сообщения на список по пробелам
        L = message.text.split()
        # Проверяем, что в списке ровно 3 элемента (валюта, валюта, количество)
        if len(L) != 3:
            raise APIException('Неверный формат команды. Попробуйте еще раз.')
        # Вызываем метод get_price класса Converter, чтобы получить результат конвертации
        ratio = Converter.get_price(L[0], L[1], L[2])
        # Составляем текст сообщения с результатом конвертации
        sss = 'Цена ' + str(L[2]) + ' ' + L[0] + ' = ' + str(ratio) + ' ' + L[1]
        # Отправляем сообщение с результатом конвертации
        bot.reply_to(message, sss)
    except APIException as e:
        # Если возникает исключение APIException, отправляем сообщение с текстом исключения
        bot.reply_to(message, str(e))
    except Exception as e:
        # Если возникает какое-то другое исключение, отправляем сообщение с текстом ошибки
        bot.reply_to(message, 'Непредвиденная ошибка:\n' + str(e) + '\nПопробуйте еще раз.')

# Запуск обработчика сообщений
bot.polling(none_stop=True)
