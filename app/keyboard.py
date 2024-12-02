from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# задаём переменую, указываем тип переменой, говорим что это 
# клавиатура, в списке клавиатуры указываем кнопку и задаём ей параметры
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="каталог"),
                                      KeyboardButton(text="Профиль")],
                                     [KeyboardButton(text="о нас"),
                                     KeyboardButton(text="регистрация")]],
                           resize_keyboard=True, input_field_placeholder='its time to choose...')


catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Диски', callback_data='disks'), InlineKeyboardButton(text='Шины', callback_data='tires')],
                                                [InlineKeyboardButton(text='На главную', callback_data='to main')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)

confB = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да',callback_data='Y'), InlineKeyboardButton(text='Нет',callback_data='N')]])

