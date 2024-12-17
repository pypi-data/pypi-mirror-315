from aiogram.types import (InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.keyboard.base_keyboards import Inline, Reply


class BaseWindow:
    text: str = "Hello, this is example message!"
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | None = None
    _size: int = 1
    _buttons = []

    def button(self, *args, keyboard: Inline | Reply = None):
        if keyboard is not None and len(args) > 0:
            raise TypeError("You should use only one keyboard")
        if keyboard is not None:
            self.reply_markup = keyboard.create()
        if len(args) == 0:
            self.reply_markup = None
            self._buttons = []
        elif len(args) == 1:
            self._buttons.append(args[0])
        elif len(args) == 2:
            self._buttons.append(args)
        else:
            raise TypeError("Unsupported format")

    def _reformat_buttons(self):
        if self._buttons:
            if all(isinstance(item, str) for item in self._buttons):
                keyboard = ReplyKeyboardBuilder()
                for button in self._buttons:
                    keyboard.add(KeyboardButton(text=button))
                self.reply_markup =  keyboard.adjust(self._size).as_markup(resize_keyboard=True)
            elif all(isinstance(item, tuple) for item in self._buttons):
                keyboard = InlineKeyboardBuilder()
                for button in self._buttons:
                    if button[1].startswith("https"):
                        keyboard.add(InlineKeyboardButton(text=button[0], url=button[1]))
                    else:
                        keyboard.add(InlineKeyboardButton(text=button[0], callback_data=button[1]))
                self.reply_markup = keyboard.adjust(self._size).as_markup()

    def size(self, size_keyboard: int):
        self._size = size_keyboard
        return self


    def _build(self):
        text = self.text
        self._reformat_buttons()
        reply_markup = self.reply_markup
        self.reply_markup = None
        return text, reply_markup











