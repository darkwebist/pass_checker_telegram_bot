# 🔐 Parol Tekshiruvchi Bot

Parol kuchini tahlil qiluvchi, brute-force buzish vaqtini hisoblovchi va foydalanuvchilarga tavsiyalar beruvchi Telegram bot.  
Yaratuvchi: **@DarkWebist** | Kanal: **@V1RU5_team**

---

## ✨ Asosiy imkoniyatlar

- **Parol kuchini baholash** – zaif, o'rtacha yoki kuchli.
- **Buzish vaqti** – 10 mlrd/s tezlikda hisoblanadi.
- **Maslahatlar** – parolni yaxshilash bo'yicha aniq tavsiyalar.
- **Statistika** – foydalanuvchi tekshiruvlar tarixi.
- **Admin panel** – barcha tekshiruvlar va foydalanuvchilar ro'yxati.

---

## 🛠 O'rnatish

1. Repozitoriyani yuklab oling yoki kodni nusxalang.
2. Kerakli kutubxonani o'rnating:
   ```bash
   pip install aiogram
   ```

3. BOT_TOKEN va ADMIN_ID ni sozlang.

---

## ⚙️ Sozlash

bot.py faylida quyidagi ikkita o'zgaruvchini o'zgartiring:

```python
BOT_TOKEN = "123456:ABC-DEF1234gh"  # @BotFather dan olingan token
ADMIN_ID = 12345678                 # Adminning Telegram ID raqami
```

---

## 🚀 Ishga tushirish

```bash
python bot.py
```

Terminalda quyidagi holat ko'rinadi:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🔐 KIBERXAVFSIZLIK BOT 🔐  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
[✓] Baza inicializatsiya qilinmoqda...
[✓] Bot handlerlari ro'yxatdan o'tilmoqda...
[✓] Tizim onlayn. Kuting...
```

---

## 📱 Foydalanish

| Tugma | Vazifasi |
|-------|----------|
| 🔐 Parol Tekshirish | Parol yuboriladi, kuchi va buzish vaqti ko'rsatiladi |
| 📊 Statistikam | O'zingizning oxirgi 10 ta tekshiruvingiz |
| ℹ️ Yordam | Kuchli parol yaratish qoidalari |

Admin foydalanuvchilari qo'shimcha 👑 Admin Panel tugmasini ko'radi.

---

## 👑 Admin panel

Admin panelida quyidagilar aks etadi:

- Umumiy foydalanuvchilar soni
- Jami tekshiruvlar soni
- Har bir foydalanuvchi, kiritilgan parol, kuch darajasi va buzish vaqti

Parollar ma'lumotlar bazasida ochiq holda saqlanadi.

---

## 🗄 Ma'lumotlar bazasi

Bot avtomatik bot_database.db faylini yaratadi va ichida ikkita jadval mavjud:

- users – foydalanuvchi ID, username, ism, qo'shilgan vaqti
- checks_log – foydalanuvchi ID, parol, natija, buzish vaqti, tekshiruv vaqti

---

## ⚠️ Xavfsizlik va javobgarlik

- Parollar lokal saqlanadi, tashqi serverga yuborilmaydi.
- Kod social engineering maqsadida yozilgan – javobgarlik butunlay foydalanuvchiga tegishli.

---

## 📡 Bog'lanish

- Yaratuvchi: @DarkWebist
- Kanal: @V1RU5_team
