from datetime import datetime
import asyncio
from aiogram.types import Message, Chat

from src.sender.sender import Send
from src.windows.base_window import BaseWindow


class HelloWindow(BaseWindow):
    def hello(self):
        self.text = "Hello, guys!"
        self.button("Hello")
        return self


chat = Chat(id=674,
            type="private")
mes = Message(message_id=23423,
              date=datetime.now(),
              chat=chat)
send = Send(event=mes)


async def check():
    await send(HelloWindow().hello())


if __name__ == '__main__':
    asyncio.run(check())