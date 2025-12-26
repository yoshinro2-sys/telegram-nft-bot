import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === НАСТРОЙКИ ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7580505769:AAE9GvLZ15h3hjtvanNwgsO2taGtRFOFNJY")
YOUR_USER_ID = 7540678453

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не установлен!")
    exit(1)

NFT_ITEMS = ["DiamondRing", "ElectricSkull", "EternalRose", "InputKey", "JellyBunny"]
is_active = False
task = None
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Начать генерацию")],
            [KeyboardButton(text="⏸️ Остановить генерацию")]
        ],
        resize_keyboard=True
    )

def generate_nft_link(nft_name):
    number = random.randint(1, 9000)
    return f"t.me/nft/{nft_name}-{number}"

async def send_links_loop():
    global is_active
    while is_active:
        try:
            for nft in NFT_ITEMS:
                if not is_active: break
                link = generate_nft_link(nft)
                await bot.send_message(chat_id=YOUR_USER_ID, text=link)
                logger.info(f"Отправлена ссылка: {link}")
                await asyncio.sleep(120)
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await asyncio.sleep(60)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != YOUR_USER_ID:
        await message.answer("⛔ У вас нет доступа!")
        return
    await message.answer("🎁 Бот для генерации NFT ссылок", reply_markup=get_keyboard())

@dp.message()
async def handle_buttons(message: types.Message):
    global is_active, task
    if message.from_user.id != YOUR_USER_ID: return
    
    if message.text == "▶️ Начать генерацию":
        if not is_active:
            is_active = True
            task = asyncio.create_task(send_links_loop())
            await message.answer("✅ Генерация начата! (каждые 2 минуты)")
    elif message.text == "⏸️ Остановить генерацию":
        if is_active:
            is_active = False
            if task: task.cancel()
            await message.answer("⏹️ Генерация остановлена!")

async def main():
    logger.info("🚀 Бот запускается...")
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
