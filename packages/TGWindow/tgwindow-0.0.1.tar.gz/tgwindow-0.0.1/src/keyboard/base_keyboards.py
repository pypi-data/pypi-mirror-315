from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder, KeyboardButton


class BaseReplyKeyboardMeta(type):
    def __new__(cls, name, bases, dct):
        buttons = []
        for key, value in dct.items():
            if not key.startswith("__") and key != "size" and key != "create":
                if not isinstance(value, str):
                    raise TypeError(f"Attribute {key} must be a string.")
                buttons.append(value)
        dct["buttons"] = buttons
        return super().__new__(cls, name, bases, dct)


class BaseInlineKeyboardMeta(type):
    def __new__(cls, name, bases, dct):
        buttons = []
        for key, value in dct.items():
            if not key.startswith("__") and key != "size" and key != "create":
                if not isinstance(value, tuple):
                    raise TypeError(f"Attribute {key} must be a tuple of (text, data/url).")
                buttons.append(value)
        dct["buttons"] = buttons
        return super().__new__(cls, name, bases, dct)


class Reply(metaclass=BaseReplyKeyboardMeta):
    size = 1

    def create(self):
        keyboard = ReplyKeyboardBuilder()
        for button in self.buttons:
            keyboard.add(KeyboardButton(text=button))
        return keyboard.adjust(self.size).as_markup(resize_keyboard=True)

    def __repr__(self):
        return "\n".join(f"text={button}" for button in self.buttons)


class Inline(metaclass=BaseInlineKeyboardMeta):
    size = 1

    def create(self):
        keyboard = InlineKeyboardBuilder()
        for button in self.buttons:
            if button[1].startswith("https"):
                keyboard.add(InlineKeyboardButton(text=button[0], url=button[1]))
            else:
                keyboard.add(InlineKeyboardButton(text=button[0], callback_data=button[1]))
        return keyboard.adjust(self.size).as_markup()

    def __repr__(self):
        lines = []
        for button in self.buttons:
            if button[1].startswith("https"):
                lines.append(f"text={button[0]}, url={button[1]}")
            else:
                lines.append(f"text={button[0]}, callback_data={button[1]}")
        return "\n".join(lines)
