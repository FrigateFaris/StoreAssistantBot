from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.crud import is_admin
from keyboards import reply
from utils.states import Form

import psycopg2
from data.config import host, user, password, db_name

router = Router()

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
)


@router.message(F.text.lower() == 'зарегистрироваться')
async def registration_user(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer('введи имя')


@router.message(F.text.lower() == 'личный кабинет')
async def office_request(message: Message):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM client_username_view;')
        users = ', '.join([str(item) for item in cursor.fetchall()])
        if message.from_user.username in users and users:
            with connection.cursor() as user_data:
                if await is_admin(message):
                    user_data.execute(f"SELECT * FROM client WHERE username = '{message.from_user.username}_admin'")
                    data = ', '.join([str(item) for item in user_data.fetchone()])
                    await message.answer(f'{data}', reply_markup=reply.start)
                else:
                    user_data.execute(f"SELECT * FROM client WHERE username = '{message.from_user.username}'")
                    data = ', '.join([str(item) for item in user_data.fetchone()])
                    await message.answer(f'{data}', reply_markup=reply.start)
        else:
            await message.answer('сначала вы должны пройти регистрацию 0_0')


@router.message(F.text.lower() == 'удалить данные')
async def delete_user_data(message: Message):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT username FROM client;')
        users = ', '.join([str(item) for item in cursor.fetchall()])
        if message.from_user.username in users:
            if await is_admin(message):
                cursor.execute(f"DELETE FROM client WHERE username = '{message.from_user.username}_admin'")
                connection.commit()
                await message.answer(f'данные успешно удалены у админа :-(', reply_markup=reply.start)
            else:
                cursor.execute(f"DELETE FROM client WHERE username = '{message.from_user.username}'")
                connection.commit()
                await message.answer(f'данные успешно удалены у клиента :-)', reply_markup=reply.start)
        else:
            await message.answer('вы еще не зарегистрированы -_-')


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)
    await message.answer('Теперь введи свой номер', reply_markup=reply.contact)


@router.message(Form.phone)
async def form_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text if message.text else message.contact.phone_number)
    await state.set_state(Form.email)
    await message.answer('Теперь введи свой email')


@router.message(Form.email)
async def form_phone(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Form.address)
    await message.answer('Теперь введи свой адресс')


@router.message(Form.address)
async def form_phone(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(address=message.location or message.text)
        data = await state.get_data()
        ready_blank = ['Вы успешно зарегестрировались! :-)\n'
                       f'name: {data["name"]}\n'
                       f'phone: {data["phone"]}\n'
                       f'email: {data["email"]}\n'
                       f'address: {data["address"]}\n']
        user_name = message.from_user.username
        if data['name'].endswith('_admin'):
            cursor.execute(f"INSERT INTO client (client_name, phone, email, client_address, username) VALUES ('{data['name']}', {(data['phone'])}, '{data['email']}', '{data['address']}', '{user_name}_admin')")
        else:
            cursor.execute(f"INSERT INTO client (client_name, phone, email, client_address, username) VALUES ('{data['name']}', {(data['phone'])}, '{data['email']}', '{data['address']}', '{user_name}')")
        connection.commit()

        await message.answer('\n'.join(ready_blank), reply_markup=reply.start)
