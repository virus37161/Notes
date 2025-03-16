from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.models import User, Note
from sqlalchemy.future import select
from datetime import datetime
from bot.keybords.keybords import kb_change_delete_notes, kb_start, kb_cancel, kb_cancel_and_skip

router = Router()

class Order(StatesGroup):
    create_name = State()
    create_content = State()
    create_term = State()
    create_reminder = State()
    change_or_delete_notes = State()
    delete_notes = State()
    change_notes = State()
    delete_note_by_id = State()
    change_note_by_id = State()

@router.message(F.text == "Проверить базу")
async def start_command(message: Message, session: AsyncSession):
    try:
        await session.execute(text("SELECT 1"))
        await message.answer("База данных работает", reply_markup=kb_start)
    except Exception:
        await message.answer("База данных не работает", reply_markup=kb_start)


@router.message(CommandStart())
async def reg_user(message: Message, session: AsyncSession):
    check_created_user = await check_user(message, session)
    if not check_created_user:
        user = User(id=message.from_user.id, name=message.from_user.username, id_chat=message.chat.id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    await message.answer(f"Добро пожаловать, {message.from_user.username}", reply_markup=kb_start)


async def check_user(message, session):
    obj = await session.execute(select(User).where(User.id == int(message.from_user.id)))
    obj = obj.scalar_one_or_none()
    return True if not obj == None else False


@router.message(F.text == "Создать заметку")
async def create_note(message: Message, state: FSMContext):
    await message.answer("Введите название", reply_markup=kb_cancel)
    await state.set_state(Order.create_name.state)


@router.message(Order.create_name)
async def create_name(message: Message, state:FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание заметки отклонено", reply_markup=kb_start)
        return None
    await state.set_data({'name': message.text})
    await message.answer("Введите содержание заметки", reply_markup=kb_cancel)
    await state.set_state(Order.create_content.state)


@router.message(Order.create_content)
async def create_term(message: Message, state:FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание заметки отклонено", reply_markup=kb_start)
        return None
    obj = await state.get_data()
    obj['content'] = message.text
    await state.set_data(obj)
    await message.answer("Введите срок, например 15.10.2025 10:30", reply_markup=kb_cancel_and_skip)
    await state.set_state(Order.create_term.state)


@router.message(Order.create_term)
async def create_reminder(message: Message, state:FSMContext):
    obj = await state.get_data()
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание заметки отклонено", reply_markup=kb_start)
        return None
    elif message.text == "Пропустить":
        await message.answer("Введите дату напоминания, например 15.10.2025 09:30", reply_markup=kb_cancel_and_skip,
                             parse_mode="Markdown")
        obj['term'] = None
        await state.set_data(obj)
        await state.set_state(Order.create_reminder.state)
    else:
        try:
            date_format = '%d.%m.%Y %H:%M'
            term = datetime.strptime(message.text, date_format)
            obj['term'] = term
            await state.set_data(obj)
            await message.answer("Введите дату напоминания, например 15.10.2025 09:30", reply_markup=kb_cancel_and_skip)
            await state.set_state(Order.create_reminder.state)
        except:
            await message.answer("Формат ввода был нарушен, попробуйте еще раз")
            await message.answer("Введите срок, например 15.10.2025 10:30", reply_markup=kb_cancel)
            await state.set_data(obj)
            await state.set_state(Order.create_term.state)




@router.message(Order.create_reminder)
async def create_obj_note(message: Message, session: AsyncSession, state:FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание заметки отклонено", reply_markup=kb_start)
        return None
    obj = await state.get_data()
    try:
        if message.text == "Пропустить":
            obj['reminder'] = None
        else:
            date_format = '%d.%m.%Y %H:%M'
            reminder = datetime.strptime(message.text, date_format)
            obj['reminder'] = reminder
        note = Note(name=obj.get('name'), content=obj.get('content'), term=obj.get('term'), reminder=obj.get('reminder'), user_id=message.from_user.id)
        session.add(note)
        await session.commit()
        await session.refresh(note)
        await message.answer("Заметка создана", reply_markup=kb_start)
        await state.clear()
    except:
        await message.answer("Формат ввода был нарушен, попробуйте еще раз")
        await message.answer("Введите дату напоминания, например 15.10.2025 09:30", reply_markup=kb_cancel)
        await state.set_data(obj)
        await state.set_state(Order.create_reminder.state)



@router.message(F.text == "Мои заметки")
async def get_my_notes(message: Message, session: AsyncSession, state:FSMContext):
    list_of_notes = await session.execute(select(Note).filter(Note.user_id==int(message.from_user.id)))
    list_of_notes = list_of_notes.scalars().all()
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb_change_delete_notes, resize_keyboard=True, one_time_keyboard=True))
    if list_of_notes:
        for note in list_of_notes:
            name = note.name
            if note.overdue:
                await message.answer(f"Название(просроч.): '{name}'\n\n\
{note.content}\n\n\
Срок: {note.term}", reply_markup=keybord)
            else:
                await message.answer(f"Название: '{name}'\n\n\
{note.content}\n\n\
Срок: {note.term}", reply_markup=keybord)
            await state.set_data({"data": list_of_notes})
            await state.set_state(Order.change_or_delete_notes.state)
    else:
        await message.answer("Заметок нет")


@router.message(Order.change_or_delete_notes)
async def change_delete_notes(message: Message, state:FSMContext, session: AsyncSession):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Вы вернулись на главную страницу", reply_markup=kb_start)
        return None
    data = await state.get_data()
    data = data.get('data')
    list_of_notes = {}
    kb_delete_notes = []
    for i in data:
        name = i.name
        id = i.id
        list_of_notes[name] = id
        kb_delete_notes.append([types.KeyboardButton(text=name)])
    kb_delete_notes.append([types.KeyboardButton(text='Отмена')])
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb_delete_notes, resize_keyboard=True, one_time_keyboard=True))
    if message.text == "Удалить заметку":
        await message.answer('Выберете заметку', reply_markup=keybord)
        await state.set_data(list_of_notes)
        await state.set_state(Order.delete_note_by_id.state)
    if message.text == "Удалить просроченные":
        await message.answer('Просроченные заметки удалены', reply_markup=kb_start)
        list_of_notes = await session.execute(select(Note).filter(Note.user_id == int(message.from_user.id), Note.overdue == True))
        list_of_notes = list_of_notes.scalars().all()
        for note in list_of_notes:
            await session.delete(note)
        await session.commit()


@router.message(Order.delete_note_by_id)
async def delete_note(message: Message, state:FSMContext, session:AsyncSession):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Вы вернулись на главную страницу", reply_markup=kb_start)
        return None
    data = await state.get_data()
    id = data.get(f'{message.text}')
    obj = await session.execute(select(Note).where(Note.id == id))
    obj = obj.scalar_one_or_none()
    await session.delete(obj)
    await session.commit()
    await message.answer('Заметка удалена', reply_markup=kb_start)


