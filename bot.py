import os
import requests
import json
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Получаем токен из Environment Variable ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Environment variable BOT_TOKEN not set!")

# --- Telegram ID для уведомлений авто ранга ---
# Можно поставить свой ID, чтобы получать уведомления
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")  # Опционально

# --- Game Service Configuration ---
FIREBASE_API_KEY = "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"
FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"
RANK_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"

# --- Аккаунты ---
ACCOUNTS = [
    {"email": "den_isaev_9595@mail.ru", "password": "Zaebali1995"},
    {"email": "cpmkingking41@gmail.com", "password": "666666"},
    {"email": "cpmkingking42@gmail.com", "password": "666666"},
]

# --- Функции для работы с аккаунтами ---
def login(email, password):
    payload = {
        "clientType": "CLIENT_TYPE_ANDROID",
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 12)",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(FIREBASE_LOGIN_URL, headers=headers, json=payload)
        data = r.json()
        if r.status_code == 200 and "idToken" in data:
            return data["idToken"]
        return None
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
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }

    try:
        r = requests.post(RANK_URL, headers=headers, json=payload)
        return r.status_code == 200
    except:
        return False

def run_rank():
    results = []
    for acc in ACCOUNTS:
        token = login(acc["email"], acc["password"])
        if token:
            if set_rank(token):
                results.append(f"✅ {acc['email']}")
            else:
                results.append(f"❌ Rank error {acc['email']}")
        else:
            results.append(f"❌ Login error {acc['email']}")
    return "\n".join(results)

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 CPM KING BOT\n\n"
        "Команды:\n"
        "/rank — запустить KING RANK вручную"
    )

async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Запуск KING RANK...")
    result = run_rank()
    await update.message.reply_text(f"👑 RESULT:\n{result}")

async def auto_rank(context: ContextTypes.DEFAULT_TYPE):
    result = run_rank()
    if TELEGRAM_ADMIN_ID:
        await context.bot.send_message(
            chat_id=TELEGRAM_ADMIN_ID,
            text=f"⏰ Авто KING RANK выполнен\n\n{result}"
        )

# --- Инициализация бота ---
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rank", rank))

# --- Ежедневный автозапуск в 03:00 ---
app.job_queue.run_daily(auto_rank, time=time(hour=3, minute=0))

# --- Запуск polling ---
app.run_polling()
