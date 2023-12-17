from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    phone = State()
    email = State()
    address = State()


class Product(StatesGroup):
    category = State()
    brands = State()


class Check(StatesGroup):
    id = State()


class Delete(StatesGroup):
    id = State()


class Update(StatesGroup):
    id = State()
    data = State()


class Add(StatesGroup):
    data = State()


class AddToCart(StatesGroup):
    title = State()


class Cart(StatesGroup):
    id = State()