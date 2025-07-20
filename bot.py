import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, ADMINS

# Настройка логирования для отслеживания работы бота
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Константа для ограничения размера файла (10 МБ в байтах)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ

# Объявление файла для хранения id пользователей
USERS_FILE = "users.txt"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Регистрация роутера в диспетчере
dp.include_router(router)

def save_user_id(user_id: int):
    """
    Сохраняет ID пользователя в файл, если его там ещё нет.
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            pass
    with open(USERS_FILE, "r+") as f:
        users = set(map(int, f.read().split()))
        if user_id not in users:
            f.write(f"{user_id}\n")

async def restrict_file_size(message: Message, file_size: int) -> bool:
    """
    Проверяет размер файла. Если он превышает MAX_FILE_SIZE, отправляет сообщение об ошибке.
    Возвращает True, если файл слишком большой, иначе False.
    """
    if file_size > MAX_FILE_SIZE:
        await message.answer(
            f"Файл слишком большой ({file_size / 1024 / 1024:.2f} МБ)! Максимальный размер: 10 МБ."
        )
        return True
    return False

async def restrict_admin(message: Message) -> bool:
    """
    Проверяет, является ли пользователь администратором. Если нет, отправляет сообщение об ошибке.
    Возвращает True, если доступ запрещён, иначе False.
    """
    if message.from_user.id not in ADMINS:
        await message.answer("Нет прав!")
        return True
    return False

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start. Отправляет приветственное сообщение пользователю.
    """
    save_user_id(message.from_user.id)
    await message.answer(
        "Привет! Я эхо-бот. Отправь мне текст, фото, стикер, видео, GIF, документ, "
        "аудио или голосовое сообщение (до 10 МБ), и я отправлю это обратно!"
    )

# Команда для вывода всех user_id
@router.message(Command("users"))
async def show_users(message: Message):
    """
    Обработчик команды /users. Выводит список ID пользователей (доступно только админам).
    """
    if await restrict_admin(message):
        return
    try:
        with open(USERS_FILE, "r") as f:
            users = f.read().strip().split()
        if users:
            await message.answer("ID пользователей:\n" + "\n".join(users))
        else:
            await message.answer("Пользователи ещё не зарегистрированы.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# Обработчик текстовых сообщений
@router.message(F.text)
async def echo_text(message: Message):
    """
    Обработчик текстовых сообщений. Повторяет полученный текст.
    """
    save_user_id(message.from_user.id)
    try:
        await message.answer(message.text)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await message.answer("Произошла ошибка, попробуйте снова!")

# Обработчик фотографий
@router.message(F.photo)
async def echo_photo(message: Message):
    """
    Обработчик фотографий. Отправляет полученную фотографию обратно, если её размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        photo = message.photo[-1]
        if await restrict_file_size(message, photo.file_size):
            return
        await message.answer_photo(photo=photo.file_id, caption=message.caption)
    except Exception as e:
        logger.error(f"Ошибка при отправке фото: {e}")
        await message.answer("Произошла ошибка при отправке фото!")

# Обработчик стикеров
@router.message(F.sticker)
async def echo_sticker(message: Message):
    """
    Обработчик стикеров. Отправляет полученный стикер обратно, если его размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.sticker.file_size):
            return
        await message.answer_sticker(sticker=message.sticker.file_id)
    except Exception as e:
        logger.error(f"Ошибка при отправке стикера: {e}")
        await message.answer("Произошла ошибка при отправке стикера!")

# Обработчик видео
@router.message(F.video)
async def echo_video(message: Message):
    """
    Обработчик видео. Отправляет полученное видео обратно, если его размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.video.file_size):
            return
        await message.answer_video(video=message.video.file_id, caption=message.caption)
    except Exception as e:
        logger.error(f"Ошибка при отправке видео: {e}")
        await message.answer("Произошла ошибка при отправке видео!")

# Обработчик анимаций (GIF)
@router.message(F.animation)
async def echo_animation(message: Message):
    """
    Обработчик анимаций (GIF). Отправляет полученную анимацию обратно, если её размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.animation.file_size):
            return
        await message.answer_animation(animation=message.animation.file_id, caption=message.caption)
    except Exception as e:
        logger.error(f"Ошибка при отправке анимации: {e}")
        await message.answer("Произошла ошибка при отправке анимации!")

# Обработчик документов
@router.message(F.document)
async def echo_document(message: Message):
    """
    Обработчик документов. Отправляет полученный документ обратно, если его размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.document.file_size):
            return
        await message.answer_document(document=message.document.file_id, caption=message.caption)
    except Exception as e:
        logger.error(f"Ошибка при отправке документа: {e}")
        await message.answer("Произошла ошибка при отправке документа!")

# Обработчик аудио
@router.message(F.audio)
async def echo_audio(message: Message):
    """
    Обработчик аудио. Отправляет полученное аудио обратно, если его размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.audio.file_size):
            return
        await message.answer_audio(audio=message.audio.file_id, caption=message.caption)
    except Exception as e:
        logger.error(f"Ошибка при отправке аудио: {e}")
        await message.answer("Произошла ошибка при отправке аудио!")

# Обработчик голосовых сообщений
@router.message(F.voice)
async def echo_voice(message: Message):
    """
    Обработчик голосовых сообщений. Отправляет полученное голосовое сообщение обратно, если его размер не превышает 10 МБ.
    """
    save_user_id(message.from_user.id)
    try:
        if await restrict_file_size(message, message.voice.file_size):
            return
        await message.answer_voice(voice=message.voice.file_id)
    except Exception as e:
        logger.error(f"Ошибка при отправке голосового сообщения: {e}")
        await message.answer("Произошла ошибка при отправке голосового сообщения!")

# Обработчик других типов сообщений
@router.message()
async def echo_unknown(message: Message):
    """
    Обработчик для неподдерживаемых типов сообщений.
    """
    save_user_id(message.from_user.id)
    await message.answer(
        "Извини, я не знаю, как обработать это сообщение! Попробуй отправить текст, "
        "фото, стикер, видео, GIF, документ, аудио или голосовое сообщение (до 10 МБ)."
    )

# Функция для запуска бота
async def main():
    """
    Основная функция для запуска бота.
    Запускает процесс опроса новых сообщений (polling).
    """
    logger.info("Бот запущен")
    await dp.start_polling(bot)

# Точка входа в программу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")