import logging
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from .keyboards import main_kb
from .states import AuthState
from .config import bot_env


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(bot_env.bot_token)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Для авторизации отправьте команду /auth",
        reply_markup=main_kb
    )


@dp.message(commands=['auth'])
async def auth_user(message: types.Message):
    await message.reply("Пожалуйста, отправьте вашу почту")
    await AuthState.waiting_for_username.set()


@dp.message(state=AuthState.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.reply("Пожалуйста, отправьте ваш пароль")
    await AuthState.waiting_for_password.set()


@dp.message(state=AuthState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    email = user_data['email']
    password = user_data['password']
    telegram_username = message.from_user.username

    try:
        response = requests.post(
            f"{bot_env.host}/auth/jwt/login",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        auth_data = response.json()
        user_id = auth_data['user']['id']  # Получаем user_id из ответа
        access_token = auth_data['access_token']  # Получаем access_token

        if auth_data['user'].get('telegram_username') is None:
            await state.update_data(user_id=user_id, access_token=access_token)
            await message.reply("Пожалуйста, отправьте ваш Telegram username")
            await AuthState.waiting_for_telegram_username.set()
        else:
            if auth_data['user']['telegram_username'] == telegram_username:
                await message.reply("Вы успешно авторизованы!")
                await state.update_data(
                    user_id=user_id,
                    access_token=access_token)
            else:
                await message.reply(
                    "Ошибка авторизации. Telegram username не совпадает."
                )
                await state.clear()
    except requests.RequestException as e:
        logger.error(f"Ошибка авторизации: {e}")
        await message.reply("Ошибка авторизации. Попробуйте снова.")
        await state.clear()


@dp.message(state=AuthState.waiting_for_telegram_username)
async def process_telegram_username(message: types.Message, state: FSMContext):
    telegram_username = message.text
    user_data = await state.get_data()
    email = user_data['email']
    user_id = user_data['user_id']

    try:
        response = requests.post(
            f"{bot_env.host}/auth/telegram",
            json={
                "telegram_username": telegram_username,
                "email": email
            },
            headers={"Authorization": f"Bearer {user_data['access_token']}"}
        )
        response.raise_for_status()
        await message.reply("Вы успешно авторизованы!")
        await state.update_data(user_id=user_id)
    except requests.RequestException as e:
        logger.error(f"Ошибка авторизации: {e}")
        await message.reply("Ошибка авторизации. Попробуйте снова.")
    finally:
        await state.clear()


@dp.message(commands=['get_task'])
async def get_task_prompt(message: types.Message):
    await message.reply("Пожалуйста, отправьте название задачи для поиска")


@dp.message(lambda message: message.text.startswith('task:'))
async def get_task_by_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    access_token = user_data['access_token']
    task_name = message.text[len('task:'):].strip()

    try:
        # Получаем все задачи пользователя
        response = requests.get(
            f"{bot_env.host}/task/tasks",
            params={"user_id": user_id},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        tasks = response.json()

        # Ищем задачу по названию
        task = next(
            (task for task in tasks if task['name'] == task_name),
            None
        )

        if task:
            task_id = task['id']
            # Получаем задачу по ID
            response = requests.get(
                f"{bot_env.host}/task/{task_id}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            task_details = response.json()
            await message.reply(
                f"Задача найдена:\nНазвание: {task_details['name']}\n"
                f"Описание: {task_details['description']}")
        else:
            await message.reply("Задача с таким названием не найдена.")
    except requests.RequestException as e:
        logger.error(f"Ошибка получения задачи: {e}")
        await message.reply("Ошибка получения задачи. Попробуйте снова.")


@dp.message(commands=['notes'])
async def get_notes(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    access_token = user_data['access_token']

    try:
        response = requests.get(
            f"{bot_env.host}/task/tasks",
            params={"user_id": user_id},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        notes = response.json()
        notes_list = "\n".join(
            [f"{note['id']}: {note['title']}" for note in notes]
        )
        await message.reply(f"Ваши заметки:\n{notes_list}")
    except requests.RequestException as e:
        logger.error(f"Ошибка получения заметок: {e}")
        await message.reply("Ошибка получения заметок. Попробуйте снова.")


@dp.message(commands=['create_note'])
async def create_note_prompt(message: types.Message):
    await message.reply(
        "Пожалуйста, отправьте заголовок и содержимое заметки"
        " в формате: Заголовок | Содержимое"
    )


@dp.message(lambda message: '|' in message.text)
async def create_note_process(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    access_token = user_data['access_token']
    title, content = message.text.split('|', 1)

    try:
        response = requests.post(
            f"{bot_env.host}/task",
            json={
                "name": title.strip(),
                "description": content.strip(),
                "user_id": user_id
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        await message.reply("Заметка успешно создана!")
    except requests.RequestException as e:
        logger.error(f"Ошибка создания заметки: {e}")
        await message.reply("Ошибка создания заметки. Попробуйте снова.")


@dp.message(commands=['search'])
async def search_notes_prompt(message: types.Message):
    await message.reply("Пожалуйста, отправьте тег для поиска заметок")


@dp.message(lambda message: message.text.startswith('#'))
async def search_notes_process(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    access_token = user_data['access_token']
    tag = message.text.strip('#').split(',')

    try:
        response = requests.get(
            f"{bot_env.host}/task/by_tag/{tag}",
            params={
                "tag": tag,
                "user_id": user_id
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        notes = response.json()
        notes_list = "\n".join(
            [f"{note['id']}: {note['title']}" for note in notes]
        )
        await message.reply(f"Найденные заметки:\n{notes_list}")
    except requests.RequestException as e:
        logger.error(f"Ошибка поиска заметок: {e}")
        await message.reply("Ошибка поиска заметок. Попробуйте снова.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(dp, skip_updates=True)
