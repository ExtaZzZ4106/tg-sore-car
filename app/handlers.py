from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq




router = Router() # аналог диспетчера но только он собирает запросы и передаёт их ему  
class REGISTER(StatesGroup):
    name = State()
    number = State()
    confirm = State()
    
# вызываем роутер говорим фильтр запроса, в скобках указываем параметр
# объявляем асинхронную функцию и задаём тип запроса
# await хз что это но он важен, указываем тип затем формат и параметры
@router.message(CommandStart())
async def cmd_start(message: Message):

    await rq.set_user(tg_id=message.from_user.id)# Запись данных в бд

    await message.reply('Добро пожаловать! Выберите пункт в меню.', reply_markup=kb.main)
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply("Как я могу помочь?")
    
@router.message(F.text == 'каталог')
async def cmd_catalog(message: Message):
    await message.answer('выберите категорию', reply_markup=kb.catalog)
    
@router.message(F.text == 'о нас')
async def cmd_about(mes: Message):
    await mes.answer(
    "Шип-Шип — магазин для людей и машин\n\n"
    "Как правило при покупке шин для своего автомобиля в интернет-магазине вы можете столкнуться с двумя подходами: качественный товар с нечеловеческим отношением. Либо человеческое отношение, но некачественный товар.\n\n"
    "Мы решили, что так быть не должно. Поэтому объединили шины высочайшего качества и действительно отличный сервис. Вот наши основные преимущества:\n\n"
    "Доставка в Тверь\n"
    "Мы отправляем шины транспортной компанией до пункта выдачи, обычно это ПЭК, КИТ или Деловые линии, но если у вас есть пожелания по выбору ТК, укажите их при оформлении заказа. Ориентировочный срок доставки указан на странице товара.\n\n"
    "Стоимость доставки вы оплачиваете при получении заказа в пункте выдачи, она зависит от размеров шин и дисков, ориентировочную сумму сообщит менеджер при подтверждении заказа. Оплатить заказ вы можете на сайте банковской картой, по квитанции в любом банке РФ или по счету с НДС при оплате юридическим лицом.\n\n"
    "Актуальный ассортимент\n"
    "Мы крайне внимательно относимся к соответствию ассортимента шин и дисков на сайте и на складе. Поэтому ситуация «есть на сайте, а в наличии нет» — для нас большая редкость.\n\n"
    "Низкие цены без подводных камней\n"
    "Обращаясь к нам, вы получите качественные шины и диски по низким ценам. И при этом никакого «серого» товара или других неприятных нюансов. Потому что мы не перекупщики. Мы — официальные партнеры лидирующих производителей!\n\n"
    "Грамотная консультация и помощь в выборе\n"
    "Ассортимент шин и дисков сейчас огромен. А преимущества тех или иных моделей зачастую не очевидны. И даже опытный автомобилист может запутаться. Но не у нас. Наши консультанты настоящие профессионалы и помогут вам выбрать оптимальный товар под задачу или бюджет.\n\n"
    "Познакомьтесь с нашей командой\n"
    "Именно эти люди будут вашими проводниками в мире шин и дисков. Можете на них положиться. Ведь их опыт действительно колоссальный. Какой бы ни был ваш вопрос, задача или потребность, они помогут на 100%.\n\n"
    "Директор на страже качества\n"
    "Наш директор Дмитрий Шмерко отвечает за качество товаров и обслуживания. Поэтому, если у вас возникла сложность или вопрос, вы можете обратиться к нему напрямую. Он лично займется вашей проблемой и обязательно найдет решение. Пишите Дмитрию на почту: director@ship-ship.ru\n\n"
    "А теперь приглашаем вас пройтись по нашему магазину и, конечно же, подобрать что-нибудь для своего автомобиля. Или сразу звоните нам\n\n"
    "8 (800) 555-15-36, поможем с выбором.",
    reply_markup=kb.main
)
  
    
    
@router.callback_query(F.data == 'disks')
async def disks(cbq: CallbackQuery):
    await cbq.answer('Диски')
    disks = await rq.select_disks()

    if disks:
        disks_text = "\n".join([f"Название: {disk.name}\n Описание: {disk.description}\n Цена: {disk.price} руб.\n\n\n" for disk in disks])
        for part in split_text(f"Категория: Диски\n\n{disks_text}"):
            await cbq.message.answer(part)
    else:
        await cbq.message.answer("В категории диски нет товаров.")

# Функция для разбиения текста на части по 4096 символов
def split_text(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]   

@router.callback_query(F.data == 'tires')
async def tires(cbq: CallbackQuery):
    await cbq.answer('Шины')
    tires = await rq.select_tires()

    if tires:
        tires_text = "\n".join([f"Название: {tire.name}\n Описание: {tire.description}\n Цена: {tire.price} руб.\n\n\n" for tire in tires])
        for part in split_text(f"Категория: Шины\n\n{tires_text}"):
            await cbq.message.answer(part)
    else:
        await cbq.message.answer("В категории шин нет товаров.")

@router.callback_query(F.data == 'to main')
async def to_main(cbq: CallbackQuery):
    await cbq.answer('На главную')
    await cbq.message.answer('категория 3', reply_markup=kb.main)


    
@router.message(F.text == 'Профиль')
async def account(message: Message):
    users = await rq.select_user(tg_id=message.from_user.id)

    if users:
        user_text = "\n".join([f"Ваше имя: {users.name}\nВаш номер: {users.number}"])
        await message.answer(user_text)
    else:
        await message.answer("Вы ещё не зарегестрированы")
    
  
    
    
@router.message(F.text == 'регистрация')
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(REGISTER.name)
    try:
        await rq.set_user(tg_id=message.from_user.id)# Запись данных в бд
    except:
        print("айди пользователя уже добавлен")
    await message.answer('Введите ваше имя')
    
@router.message(REGISTER.name)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(REGISTER.number)
    await message.answer('Введите ваш номер телефона', reply_markup=kb.get_number)


@router.message(REGISTER.number, F.contact)
async def reg_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.set_state(REGISTER.confirm)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш номер: {data["number"]}', reply_markup=kb.confB)


@router.callback_query(F.data == 'Y')
async def confirm_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await rq.select_user(tg_id=callback.from_user.id)

    if user.name != data["name"] or user.number != data["number"]:
        if not user.name or not user.number:
            await rq.set_full_user(tg_id=callback.from_user.id, name=data['name'], number=data['number'])  # Запись данных в бд

            await callback.answer('Данные успешно сохранены!')
            await callback.message.answer('Данные успешно сохранены!', reply_markup=kb.main)
            await state.clear()
        else:
            await callback.answer('Необходино заполнить все поля')
            await state.clear()
    else:
        await callback.answer('Вы уже были зарегестрированы')
        await state.clear()

@router.callback_query(F.data == 'N')
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отмена успешна')
    await callback.message.answer('Отмена успешна', reply_markup=kb.main)
    await state.clear()