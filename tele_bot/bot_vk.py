# bot_vk.py — VK-версия с получением имени пользователя
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from vkbottle.bot import Bot, Message
from vkbottle.tools import Keyboard, KeyboardButtonColor, Text, OpenLink

# Загрузка переменных из .env
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

VK_TOKEN = os.getenv("VK_TOKEN")
REGISTRATION_URL = os.getenv("REGISTRATION_URL", "https://flask.cubinez.ru")

if not VK_TOKEN:
    raise ValueError("⚠️ VK_TOKEN не найден в .env!")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(VK_TOKEN)

# === Функция: получение имени пользователя по ID ===
async def get_user_name(user_id: int) -> str:
    """Получает имя пользователя через API VK"""
    try:
        # API-запрос к users.get
        response = await bot.api.users.get(user_ids=user_id, fields="first_name")
        if response:
            return response[0].first_name
    except Exception as e:
        logger.error(f"Не удалось получить имя пользователя {user_id}: {e}")
    
    # Fallback, если имя не удалось получить
    return "друг"

# === Клавиатуры ===

def keyboard_registration_step1():
    """Клавиатура с кнопкой 'Кнопка' (шаг 1)"""
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text("🔗 Кнопка"), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def keyboard_with_url_button(url: str):
    """Клавиатура с кнопкой, открывающей внешнюю ссылку"""
    return (
        Keyboard(one_time=False, inline=True)
        .add(OpenLink(url, label="🌐 Перейти на сайт"), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )

def keyboard_registration_step2():
    """Клавиатура с кнопкой 'Кнопка 2' (шаг 2, исчезает после нажатия)"""
    return (
        Keyboard(one_time=True, inline=False)
        .add(Text("✅ Кнопка 2"), color=KeyboardButtonColor.POSITIVE)
        .get_json()
    )

def keyboard_start():
    """Простая клавиатура для fallback"""
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text("🔗 Кнопка"), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )

# === Обработчик /start или "привет" ===
@bot.on.message(text=["привет", "Привет", "/старт", "/start", "старт"])
async def start_handler(message: Message):
    logger.info(f"📩 Start от {message.from_id}")
    
    # ✅ Получаем имя пользователя через API
    user_name = await get_user_name(message.from_id)
    
    await message.answer(f"Привет, {user_name}! 👋")
    
    await message.answer(
        "Для регистрации на сайте нажмите на кнопку ниже:",
        keyboard=keyboard_registration_step1()
    )

# === Обработчик "Кнопка" ===
@bot.on.message(text=["Кнопка", "🔗 Кнопка"])
async def button1_handler(message: Message):
    logger.info(f"🔘 Кнопка 1 нажата от {message.from_id}")
    
    await message.answer(
        f"Перейдите по ссылке для регистрации:\n{REGISTRATION_URL}",
        keyboard=keyboard_with_url_button(REGISTRATION_URL)
    )
    
    await message.answer(
        "После регистрации нажмите на кнопку ниже, чтобы завершить:",
        keyboard=keyboard_registration_step2()
    )

# === Обработчик "Кнопка 2" ===
@bot.on.message(text=["Кнопка 2", "✅ Кнопка 2"])
async def button2_handler(message: Message):
    logger.info(f"✅ Кнопка 2 нажата от {message.from_id}")
    
    # ✅ Тоже персонализируем ответ
    user_name = await get_user_name(message.from_id)
    await message.answer(f"Спасибо за регистрацию, {user_name}! 🎉")

# === Все остальные сообщения ===
@bot.on.message()
async def fallback_handler(message: Message):
    logger.info(f"❓ Неизвестная команда от {message.from_id}: {message.text}")
    
    await message.answer(
        "Нажмите /start для начала регистрации.",
        keyboard=keyboard_start()
    )

# === Запуск ===
if __name__ == "__main__":
    logger.info("🚀 VK Registration Bot starting...")
    bot.run_forever()
