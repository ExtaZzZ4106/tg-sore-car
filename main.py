import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.handlers import router #импортируем роутер из hendlers для передачи запросов
from app.database.models import async_main

    


#главная функция которая запускает проект
async def main():
    await async_main()
    bot = Bot(token='YOUR_TOKEN')# токен тг бота
    dp = Dispatcher()# сам диспетчер
    dp.include_router(router)#здесь передаём диспетчеру запросы из папки handlers благодоря роутеру
    await dp.start_polling(bot)#здесь говорим что диспетчер должен проверять не пришли ли новые сообщения

if __name__ == "__main__":
    try:
        asyncio.run(main())#запускаем главную функцию
    except KeyboardInterrupt:
        print('Бот выключен')