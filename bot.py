import os
import requests
import json
from datetime import time
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Токен через Environment Variable ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Environment variable BOT_TOKEN not set!")

# --- Настройки игры ---
FIREBASE_API_KEY = "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"
FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"
RANK_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"

# --- Аккаунты ---
ACCOUNTS = [
    {"email": "den_isaev_9595@mail.ru", "password": "Zaebali1995"},
    {"email": "cpmkingking41@gmail.com", "password": "666666"},
    {"email": "cpmkingking42@gmail.com", "password": "666666"},
]

# --- Функции работы с аккаунтами ---
def login(email, password):
    payload = {
        "clientType": "CLIENT_TYPE_ANDROID",
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {"User-Agent": "Dalvik/2.1.0", "Content-Type": "application/json"}
    try:
        r = requests.post(FIREBASE_LOGIN_URL, headers=headers, json=payload)
        data = r.json()
        return data.get("idToken") if r.status_code == 200 else None
    except:
        return None

def set_rank(token):
    rating_data = {k: 100000 for k in [
        "cars","car_fix","car_collided","car_exchange","car_trade","car_wash",
        "slicer_cut","drift_max","drift","cargo","delivery","taxi","levels",
        "gifts","fuel","offroad","speed_banner","reactions","police","run",
        "real_estate","t_distance","treasure","block_post","push_ups",
        "burnt_tire","passanger_distance"
    ]}
    rating_data["time"] = 10000000000
    rating_data["race_win"] = 3000

    payload = {"data": json.dumps({"RatingData": rating_data})}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "okhttp/3.12.13"}
    try:
        r = requests.post(RANK_URL, headers=headers, json=payload)
        return r.status_code == 200
    except:
        return False

def run_rank():
    success_count = 0
    for acc in ACCOUNTS:
        token = login(acc["email"], acc["password"])
        if token and set_rank(token):
            success_count += 1
    return success_count, len(ACCOUNTS)

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Запуск KING RANK...")
    success, total = run_rank()
    await update.message.reply_text(f"👑 KING RANK выполнен!\nУспешно: {success}/{total} аккаунтов")

# --- Авто запуск по расписанию ---
async def scheduled_rank(context: ContextTypes.DEFAULT_TYPE):
    success, total = run_rank()
    print(f"Авто KING RANK выполнен: {success}/{total} аккаунтов")  # Логи на Render

# --- Инициализация бота ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# --- Таймзона Москва ---
moscow_tz = pytz.timezone("Europe/Moscow")

# --- Запуск ежедневно в 23:40 по Москве ---
app.job_queue.run_daily(scheduled_rank, time=time(hour=23, minute=40, tzinfo=moscow_tz))

# --- Запуск polling ---
app.run_polling()
