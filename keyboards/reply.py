from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButtonRequestUser

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='перейти к магазину'),
            KeyboardButton(text='зарегистрироваться'),
        ],
        [
            KeyboardButton(text='личный кабинет'),
            KeyboardButton(text='удалить данные')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
)

market = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='добавить продукт'),
            KeyboardButton(text='посмотреть продукты'),
            KeyboardButton(text='посмотреть продукт'),
        ],
        [
            KeyboardButton(text='удалить продукт'),
            KeyboardButton(text='обновить продукт'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
)

client_market = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='посмотреть продукты'),
            KeyboardButton(text='посмотреть продукт'),
        ],
        [
            KeyboardButton(text='корзина'),
            KeyboardButton(text='добавить продукт в корзину'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться контактом', request_contact=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
)

product_category = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='все продукты'),
            KeyboardButton(text='10 из последних добавленных продуктов'),
        ],
        [
            KeyboardButton(text='все продукты определенной категории'),
            KeyboardButton(text='все продукты определенного бренда'),
        ],
        [
            KeyboardButton(text='перейти к магазину'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберете действие из меню',
)
