from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types

kb_change_delete_notes = [[types.KeyboardButton(text="Удалить заметку")], [types.KeyboardButton(text = "Удалить просроченные")], [types.KeyboardButton(text = "Отмена")]]
start = [[types.KeyboardButton(text="Создать заметку")], [types.KeyboardButton(text = "Мои заметки")]]
cancel = [[types.KeyboardButton(text="Отмена")]]
cancel_and_skip = [[types.KeyboardButton(text="Отмена")], [types.KeyboardButton(text = "Пропустить")]]

kb_start = (types.ReplyKeyboardMarkup(keyboard=start, resize_keyboard=True, one_time_keyboard=True))
kb_cancel = (types.ReplyKeyboardMarkup(keyboard=cancel, resize_keyboard=True, one_time_keyboard=True))
kb_cancel_and_skip = (types.ReplyKeyboardMarkup(keyboard=cancel_and_skip, resize_keyboard=True, one_time_keyboard=True))