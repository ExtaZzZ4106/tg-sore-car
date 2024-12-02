# tg-store-car

# Документация для проекта на Aiogram с использованием SQLAlchemy

## Описание проекта

Проект представляет собой Telegram-бота, использующего библиотеку **Aiogram** для взаимодействия с пользователем через Telegram API и **SQLAlchemy** для работы с базой данных. Бот предлагает пользователям выбрать товары из каталога (например, шины и диски), пройти регистрацию и просматривать свой профиль. Пользовательские данные сохраняются в базе данных SQLite, а для взаимодействия с ботом используются кастомные клавиатуры и кнопки. Бот поддерживает команды для старта, помощи и управления профилем.

---

# Инструкция по установке

Для того чтобы запустить Telegram-бота, выполните следующие шаги:

## Шаг 1: Клонирование репозитория

Склонируйте репозиторий проекта на свой локальный компьютер с помощью следующей команды:

```bash
git clone https://github.com/ExtaZzZ4106/tg-store-car.git
```

## Шаг 2: Установка зависимостей

Перейдите в каталог с проектом и установите все необходимые зависимости, используя pip:
```bash
cd <папка_проекта>
pip install aiogram sqlalchemy aiosqlite
```
## Шаг 3: Создание и настройка базы данных
- Убедитесь, что у вас установлен SQLite.
- База данных будет автоматически создана при первом запуске бота (используется файл db.sqlite3).
- Для удобного редактирования бд используйте (SQLiteStudio)[https://sqlitestudio.pl/]

## Шаг 4: Настройка токена бота
- В файле main.py или в другом конфигурационном файле проекта укажите токен вашего бота, полученный через (BotFather)[https://telegram.me/BotFather]:

## Шаг 5: Запуск проекта
Запустите бота с помощью команды:
```bash
python main.py
```


После этого бот начнёт работать и будет доступен для взаимодействия в Telegram.




## Модели базы данных (`app/database/models.py`)

### User
Модель пользователя для хранения данных пользователей Telegram:
  ```bash
  class User(Base):
        __tablename__ = 'users'
    
        id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
        tg_id = mapped_column(BigInteger, nullable=True)
        name: Mapped[str] = mapped_column(String(30), nullable=True)
        number: Mapped[str] = mapped_column(nullable=True)
  ```
### Описание:
- id: Идентификатор пользователя, первичный ключ.
- tg_id: Идентификатор Telegram пользователя.
- name: Имя пользователя.
- number: Номер телефона пользователя.

### Category
Модель категории товаров:
  ```bash
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=True)

  ```
### Описание:
- id: Идентификатор категории, первичный ключ.
- name: Название категории.

### Item
Модель товара, связанная с категорией через внешний ключ:
  ```bash
class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    description: Mapped[str] = mapped_column(String(120), nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=True)


  ```

### Описание:
- id: Идентификатор товара, первичный ключ.
- name: Название товара.
- description: Описание товара.
- price: Цена товара.
- category_id: Идентификатор категории товара (внешний ключ).





## Запросы к базе данных (app/database/requests.py)
### set_user(tg_id)
Добавляет пользователя в базу данных, если он ещё не существует.
  ```bash
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

  ```
### Описание:
- tg_id (int): Идентификатор пользователя Telegram.
- Добавляет пользователя в базу данных, если его нет.



### set_full_user(tg_id, name, number)
Обновляет данные пользователя (имя и номер) в базе данных.

  ```bash
async def set_full_user(tg_id, name, number):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            if user.name != name and user.number != number:
                user.name = name
                user.number = number
                session.add(user)
                await session.commit()
            else:
                print("Такой пользователь уже существует")
        else:
            print("такого id не существует")


  ```

### Описание:
- tg_id (int): Идентификатор пользователя Telegram.
- name (str): Имя пользователя.
- number (str): Номер телефона пользователя.
- Обновляет данные пользователя в базе данных.

### select_user(tg_id)
Получает информацию о пользователе по его tg_id.

  ```bash
async def select_user(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar()
        return user

  ```

### Описание:
- tg_id (int): Идентификатор пользователя Telegram.
- Возвращает объект пользователя из базы данных.

### select_tires()
Получает все товары, относящиеся к категории "Шины" (category_id = 1).
  ```bash
async def select_tires():
    async with async_session() as session:
        result = await session.execute(select(Item).where(Item.category_id == 1))
        tires = result.scalars().all()
        return tires

  ```
### Описание:
- Возвращает все товары в категории "Шины".

### select_disks()
Получает все товары, относящиеся к категории "Диски" (category_id = 2).
  ```bash
async def select_disks():
    async with async_session() as session:
        result = await session.execute(select(Item).where(Item.category_id == 2))
        disks = result.scalars().all()
        return disks

  ```

Заключение
Этот проект предоставляет базовый функционал для бота, который может быть расширен для работы с более сложными категориями товаров и интеграциями с другими сервисами.



