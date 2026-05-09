
# 🔐 KiberXavfsizlik Bot

<p align="center">
  <img src="https://via.placeholder.com/150?text=%F0%9F%94%90" alt="Logo" width="150"/>
</p>

<p align="center">
  <b>Telegram bot · Parol kuchini baholash · Social Engineering</b><br>
  <code>Yaratuvchi: @DarkWebist</code> | <code>Kanal: @V1RU5_team</code>
</p>

---

## 📋 Mundarija
- [Imkoniyatlar](#imkoniyatlar)
- [O‘rnatish](#o‘rnatish)
- [Sozlash](#sozlash)
- [Ishga tushirish](#ishga-tushirish)
- [Foydalanish](#foydalanish)
- [Ma’lumotlar bazasi](#ma’lumotlar-bazasi)
- [Xavfsizlik](#xavfsizlik)
- [Admin panel](#admin-panel)
- [Bog‘lanish](#bog‘lanish)

---

## 🚀 Imkoniyatlar
- 🔍 **Parol kuchini aniqlash** — zaif, o‘rtacha, kuchli deb baholaydi.
- ⏱️ **Brute-force buzish vaqtini hisoblash** — soniyalardan milliard yillargacha.
- 📊 **Statistika** — foydalanuvchi shaxsiy tekshiruvlar tarixi.
- 👑 **Admin panel** — barcha tekshirilgan parollarni va foydalanuvchilarni ko‘rish.
- 📝 **Maslahatlar** — parolni yaxshilash bo‘yicha aniq tavsiyalar.
- 🔐 **SQLite bazasi** — tekshiruvlar va foydalanuvchilar saqlanadi.

## ⚙️ O‘rnatish

### Talablar
- Python 3.10+
- `pip` paket menejeri

### 1. Repozitoriyani yuklab oling
```bash
git clone <repo-link> && cd <project-folder>
```

yoki kodni qo‘lda nusxalang.

2. Kutubxonalarni o‘rnating

```bash
pip install aiogram
```

sqlite3, asyncio, re, datetime standart kutubxonada mavjud.

🔧 Sozlash

bot.py ichida ikkita o‘zgaruvchini o‘zgartiring:

```python
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"     # @BotFather dan oling
ADMIN_ID = 123456789                      # Admin Telegram ID raqamingiz
```

▶️ Ishga tushirish

```bash
python bot.py
```

Terminalda quyidagi chiqadi:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🔐 KIBERXAVFSIZLIK BOT 🔐  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
[✓] Baza inicializatsiya qilinmoqda...
[✓] Bot handlerlari ro'yxatdan o'tilmoqda...
[✓] Tizim onlayn. Kuting...
```

📱 Foydalanish

Tugma Tavsif
🔐 Parol Tekshirish Parol kuchini va buzish vaqtini ko‘rsatadi
📊 Mening Statistikam Shaxsiy tekshiruvlar tarixi (oxirgi 10 ta)
ℹ️ Yordam Qo‘llanma va kuchli parol qoidalari
👑 Admin Panel faqat ADMIN_ID uchun – to‘liq loglar va statistika

Admin panelida har bir foydalanuvchi, kiritilgan parol, kuch darajasi va vaqt to‘liq ko‘rinadi.

🗄️ Ma’lumotlar bazasi

Bot ishga tushganda avtomatik bot_database.db yaratadi:

· users – foydalanuvchilar (user_id, username, first_name, joined_at)
· checks_log – barcha tekshiruvlar (id, user_id, username, password, strength_result, crack_time, check_time)

Parollar ochiq holda saqlanadi – admin ularni ko‘ra oladi.

🛡️ Xavfsizlik

· Parol hech qanday tashqi serverga yuborilmaydi, lokal bazada qoladi.
· Baza fayli bot joylashgan papkada (bot_database.db) saqlanadi – uni himoya qilish adminning vazifasi.
· Bot logikasi password o‘zgaruvchisini to‘g‘ridan-to‘g‘ri qayta ishlaydi, manipulyatsiyaga moyil bo‘lmasligi uchun kod kiritish tekshirilmaydi.

📡 Bog‘lanish

· Yaratuvchi: @DarkWebist
· Rasmiy kanal: @V1RU5_team

---

Bu kod social engineering maqsadlarida yozilgan. Barcha javobgarlik foydalanuvchida.
