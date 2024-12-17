import logging

from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from pydantic_core import ValidationError

from src.windows.base_window import BaseWindow


class Send:
    def __init__(self, event: Message | CallbackQuery):
        self.event: Message | CallbackQuery = event
        self.text: str = ""
        self.reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | None = None
        self.photo: str | None = None

    async def _sender(self):
        if isinstance(self.event, Message):
            await self._is_message()
        else:
            await self._is_callback()

    async def _is_message(self):
        if self.photo is not None:
            await self.event.answer_photo(photo=self.photo, caption=self.text, reply_markup=self.reply_markup)
        else:
            await self.event.answer(text=self.text, reply_markup=self.reply_markup)

    async def _is_callback(self):
        self.event: CallbackQuery
        try:
            if self.event.message.caption is not None:
                await self.event.message.edit_caption(caption=self.text, reply_markup=self.reply_markup)
            else:
                await self.event.message.edit_text(text=self.text, reply_markup=self.reply_markup)
        except ValidationError:
            logging.warning("Mistake with keyboard deleting")


    async def __call__(self,
                       window: BaseWindow | tuple[str, ReplyKeyboardMarkup | InlineKeyboardMarkup | None] | str,
                       photo: str | None = None):
        if isinstance(window, BaseWindow):
            self.text, self.reply_markup = window._build()
        elif isinstance(window, tuple):
            self.text, self.reply_markup = window
        elif isinstance(window, str):
            self.text, self.reply_markup = window, None
        else:
            raise TypeError("Unsupported type")
        self.photo = photo
        await self._sender()