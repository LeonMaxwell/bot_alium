from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('Сила языка')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1)

b2 = KeyboardButton("Информация о персонаже")
kb_client1 = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client1.add(b1).add(b2)