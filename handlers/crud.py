from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import psycopg2
from data.config import host, user, password, db_name

from keyboards import reply
from utils.states import Check, Delete, Update, Add, Product

router = Router()

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
)


async def is_admin(message):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM client WHERE username LIKE '%_admin'")
        users = ', '.join([str(item) for item in cursor.fetchall()])
        if users and message.from_user.username in users:
            return True
        else:
            return False


@router.message(F.text.lower() == 'перейти к магазину')
async def check_products(message: Message):
    if await is_admin(message):
        await message.answer('О, вы админ :-)\nСмотри сколько нопок\nили назад командой /start', reply_markup=reply.market)
    else:
        await message.answer('К сожалению вы не админ :-(\nу вас ограниченные кнопки\nили назад командой /start', reply_markup=reply.client_market)


# view -----------------------------------------------------------------------------------------------------------------

# view add product
@router.message(F.text.lower() == 'добавить продукт')
async def add_product(message: Message, state: FSMContext):
    await state.set_state(Add.data)
    await message.answer(f'Введи данные продукта в виде\ntitle, category_id, brand_id, price, product_description', reply_markup=reply.market)


# view check product
@router.message(F.text.lower() == 'посмотреть продукт')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(Check.id)
    if await is_admin(message):
        await message.answer('Введи UUID продукта', reply_markup=reply.market)
    else:
        await message.answer('Введи UUID продукта', reply_markup=reply.client_market)


# view delete product
@router.message(F.text.lower() == 'удалить продукт')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(Delete.id)
    await message.answer(f'Введи UUID продукта', reply_markup=reply.market)


# view update product
@router.message(F.text.lower() == 'обновить продукт')
async def update_product(message: Message, state: FSMContext):
    await state.set_state(Update.id)
    await message.answer(f'Введи UUID продукта', reply_markup=reply.market)

# ----------------------------------------------------------------------------------------------------------------------


# view all categories in the category 'products' -----------------------------------------------------------------------

@router.message(F.text.lower() == 'посмотреть продукты')
async def show_product_category(message: Message):
    await message.answer('здесь тоже выбрать надо ;-)', reply_markup=reply.product_category)


# view all products
@router.message(F.text.lower() == 'все продукты')
async def get_all_products(message: Message):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM all_products_view;')
        products = ', '.join([f'{item}\n\n' for item in cursor.fetchall()])
        await message.answer(f'{products}', reply_markup=reply.product_category)


# view last products
@router.message(F.text.lower() == '10 из последних добавленных продуктов')
async def get_last_added_products(message: Message):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM GetLatestProducts();')
        products = ', '.join([f'{item}\n' for item in cursor.fetchall()])
        await message.answer(f'{products}', reply_markup=reply.product_category)


# view all products current category
@router.message(F.text.lower() == 'все продукты определенной категории')
async def definite_category_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM all_category_view;')
        products = ', '.join([f'{item}\n' for item in cursor.fetchall()])
        await state.set_state(Product.category)
        await message.answer(f'{products}\n\nВыбери ID категории', reply_markup=reply.product_category)


# view all products current brand
@router.message(F.text.lower() == 'все продукты определенного бренда')
async def definite_brand_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM all_brand_view;')
        products = ', '.join([f'{item}\n' for item in cursor.fetchall()])
        await state.set_state(Product.brands)
        await message.answer(f'{products}\n\nВыбери ID бренда', reply_markup=reply.product_category)

# ----------------------------------------------------------------------------------------------------------------------


# create delete update -------------------------------------------------------------------------------------------------

@router.message(Add.data)
async def add_product_by_datas(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(data={"data": message.text})
        data = message.text.split(', ')
        cursor.execute(f"SELECT insert_product('{data[0]}', {int(data[1])}, {int(data[2])}, {int(data[3])}, '{data[4]}')")
        connection.commit()
        await message.answer(f'Вы успешно добавили продукт\n{message.text}\nУрa! :-)', reply_markup=reply.market)


@router.message(Delete.id)
async def delete_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT delete_product_by_uuid('{message.text}')")
        await message.answer(f'Выбранный продукт с UUID {message.text} успешно удален :-(', reply_markup=reply.market)


last = None


@router.message(Update.id)
async def update_product_request(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        global last
        last = message.text
        await state.update_data(id=message.text)
        await state.set_state(Update.data)
        cursor.execute(f"SELECT * FROM select_product_by_uuid('{message.text}')")
        product = ', '.join([str(item) for item in cursor.fetchone()])
        await message.answer(f'Выбранный продукт: {product}\nВведи новые данные продукта в виде\ntitle, category_id, brand_id, price, product_description')


@router.message(Update.data)
async def update_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(data={"data": message.text})
        data = message.text.split(', ')
        cursor.execute(f"SELECT update_product_by_uuid('{data[0]}', {int(data[1])}, {int(data[2])}, {int(data[3])}, '{data[4]}', '{last}')")
        await message.answer(f'Выбранный продукт с {message.text}:\n успешно обновлен\nЮхууу :-)', reply_markup=reply.market)

# ----------------------------------------------------------------------------------------------------------------------


# check product func----------------------------------------------------------------------------------------------------

@router.message(Check.id)
async def get_title_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT * FROM get_product_info_by_uuid('{message.text}')")
        products = ' '.join([str(f'{item}\n') for item in cursor.fetchone()])
        if await is_admin(message):
            await message.answer(f'Информация о продукте с UUID "{message.text}":\n{products}', reply_markup=reply.market)
        else:
            await message.answer(f'Информация о продукте с UUID "{message.text}":\n{products}', reply_markup=reply.client_market)


@router.message(Product.category)
async def get_product_category(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(category=message.text)
        cursor.execute(f"SELECT * FROM get_products_by_category_id({message.text})")
        products = ', '.join([str(item) for item in cursor.fetchall()])
        await message.answer(f'все продукты с категорией {message.text}: {products}', reply_markup=reply.product_category)


@router.message(Product.brands)
async def get_products_brand(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(category=message.text)
        cursor.execute(f"SELECT * FROM get_products_by_brand_id({message.text})")
        products = ', '.join([str(item) for item in cursor.fetchall()])
        await message.answer(f'все продукты с брендом {message.text}: {products}', reply_markup=reply.product_category)

# ----------------------------------------------------------------------------------------------------------------------

