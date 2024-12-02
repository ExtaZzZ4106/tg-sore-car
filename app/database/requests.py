from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select
from aiogram.types import Message

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))

            await session.commit()

async def set_full_user(tg_id, name, number):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        #Name = await session.scalar(select(User).where(User.name == name))
        #Number = await session.scalar(select(User).where(User.number == number))
    
        if user:
            if user.name != name and user.number != number:
                user.name = name
                user.number = number
                session.add(user)
                await session.commit()
                print("Данные пользователя обновлены.")
            else:
                print("Такой пользователь уже существует")
        else:
            print("такого id не существует")
async def select_user(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar()
        return user
    
async def select_tires():
    async with async_session() as session:
        result = await session.execute(select(Item).where(Item.category_id == 1))
        tires = result.scalars().all()
        return tires
    
async def select_disks():
    async with async_session() as session:
        result = await session.execute(select(Item).where(Item.category_id == 2))
        disks = result.scalars().all()
        return disks



