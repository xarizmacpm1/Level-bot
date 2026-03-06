import os
import requests
import json
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Token через Environment Variable ---
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
    {"email": "sultanabdulaev2006@gmail.com", "password": "31072006"},
    {"email": "cpmcpmking1@gmail.com", "password": "666666"},
    {"email": "cpmcpmking2@gmail.com", "password": "666666"},
    {"email": "cpmcpmking3@gmail.com", "password": "666666"},
    {"email": "cpmcpmking4@gmail.com", "password": "666666"},
    {"email": "cpmcpmking5@gmail.com", "password": "666666"},
    {"email": "cpmcpmking6@gmail.com", "password": "666666"},
    {"email": "cpmcpmking7@gmail.com", "password": "666666"},
    {"email": "cpmcpmking88@gmail.com", "password": "666666"},
    {"email": "cpmcpmking9@gmail.com", "password": "666666"},
    {"email": "cpmcpmking10@gmail.com", "password": "666666"},
    {"email": "cpmcpmking11@gmail.com", "password": "666666"},
    {"email": "cpmcpmking12@gmail.com", "password": "666666"},
    {"email": "cpmcpmking13@gmail.com", "password": "666666"},
    {"email": "cpmcpmking14@gmail.com", "password": "666666"},
    {"email": "cpmcpmking15@gmail.com", "password": "666666"},
    {"email": "cpmcpmking16@gmail.com", "password": "666666"},
    {"email": "cpmcpmking17@gmail.com", "password": "666666"},
    {"email": "cpmcpmking188@gmail.com", "password": "666666"},
    {"email": "cpmcpmking19@gmail.com", "password": "666666"},
    {"email": "cpmcpmking20@gmail.com", "password": "666666"},
    {"email": "cpmcpmking21@gmail.com", "password": "666666"},
    {"email": "cpmcpmking22@gmail.com", "password": "666666"},
    {"email": "cpmcpmking23@gmail.com", "password": "666666"},
    {"email": "cpmcpmking24@gmail.com", "password": "666666"},
    {"email": "cpmcpmking25@gmail.com", "password": "666666"},
    {"email": "cpmcpmking26@gmail.com", "password": "666666"},
    {"email": "cpmcpmking27@gmail.com", "password": "666666"},
    {"email": "cpmcpmking28@gmail.com", "password": "666666"},
    {"email": "cpmcpmking29@gmail.com", "password": "666666"},
    {"email": "cpmcpmking30@gmail.com", "password": "666666"},
    {"email": "cpmcpmking31@gmail.com", "password": "666666"},
    {"email": "cpmcpmking32@gmail.com", "password": "666666"},
    {"email": "cpmcpmking33@gmail.com", "password": "666666"},
    {"email": "cpmcpmking34@gmail.com", "password": "666666"},
    {"email": "cpmcpmking35@gmail.com", "password": "666666"},
    {"email": "cpmcpmking36@gmail.com", "password": "666666"},
    {"email": "cpmcpmking37@gmail.com", "password": "666666"},
    {"email": "cpmcpmking388@gmail.com", "password": "666666"},
    {"email": "cpmcpmking39@gmail.com", "password": "666666"},
    {"email": "cpmcpmking40@gmail.com", "password": "666666"},
    {"email": "cpmcpmking41@gmail.com", "password": "666666"},
    {"email": "cpmcpmking42@gmail.com", "password": "666666"},
    {"email": "cpmcpmking43@gmail.com", "password": "666666"},
    {"email": "cpmcpmking44@gmail.com", "password": "666666"},
    {"email": "cpmcpmking45@gmail.com", "password": "666666"},
    {"email": "cpmcpmking46@gmail.com", "password": "666666"},
    {"email": "cpmcpmking47@gmail.com", "password": "666666"},
    {"email": "cpmcpmking48@gmail.com", "password": "666666"},
    {"email": "cpmcpmking49@gmail.com", "password": "666666"},
    {"email": "cpmcpmking50@gmail.com", "password": "666666"},
    {"email": "cpmcpmking51@gmail.com", "password": "666666"},
    
    {"email": "den_isaev_95@mail.ru", "password": "Zaebali1995"},
    {"email": "kingcpmcpm1@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm2@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm3@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm4@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm5@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm6@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm7@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm88@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm9@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm10@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm11@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm12@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm13@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm14@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm15@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm16@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm17@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm188@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm19@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm20@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm21@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm22@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm23@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm24@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm25@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm26@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm27@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm28@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm29@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm30@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm31@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm32@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm33@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm34@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm35@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm36@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm37@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm388@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm39@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm40@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm41@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm42@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm43@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm44@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm45@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm46@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm47@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm48@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm49@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm50@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm51@gmail.com", "password": "666666"},
    {"email": "kingcpmcpm52@gmail.com", "password": "666666"},
    
    {"email": "cpmkingking1@gmail.com", "password": "666666"},
    {"email": "cpmkingking2@gmail.com", "password": "666666"},
    {"email": "cpmkingking3@gmail.com", "password": "666666"},
    {"email": "cpmkingking4@gmail.com", "password": "666666"},
    {"email": "cpmkingking5@gmail.com", "password": "666666"},
    {"email": "cpmkingking6@gmail.com", "password": "666666"},
    {"email": "cpmkingking7@gmail.com", "password": "666666"},
    {"email": "cpmkingking8@gmail.com", "password": "666666"},
    {"email": "cpmkingking9@gmail.com", "password": "666666"},
    {"email": "cpmkingking10@gmail.com", "password": "666666"},
    {"email": "cpmkingking11@gmail.com", "password": "666666"},
    {"email": "cpmkingking12@gmail.com", "password": "666666"},
    {"email": "cpmkingking13@gmail.com", "password": "666666"},
    {"email": "cpmkingking14@gmail.com", "password": "666666"},
    {"email": "cpmkingking15@gmail.com", "password": "666666"},
    {"email": "cpmkingking16@gmail.com", "password": "666666"},
    {"email": "cpmkingking17@gmail.com", "password": "666666"},
    {"email": "cpmkingking18@gmail.com", "password": "666666"},
    {"email": "cpmkingking19@gmail.com", "password": "666666"},
    {"email": "cpmkingking20@gmail.com", "password": "666666"},
    {"email": "cpmkingking21@gmail.com", "password": "666666"},
    {"email": "cpmkingking22@gmail.com", "password": "666666"},
    {"email": "cpmkingking23@gmail.com", "password": "666666"},
    {"email": "cpmkingking24@gmail.com", "password": "666666"},
    {"email": "cpmkingking25@gmail.com", "password": "666666"},
    {"email": "cpmkingking26@gmail.com", "password": "666666"},
    {"email": "cpmkingking27@gmail.com", "password": "666666"},
    {"email": "cpmkingking28@gmail.com", "password": "666666"},
    {"email": "cpmkingking29@gmail.com", "password": "666666"},
    {"email": "cpmkingking30@gmail.com", "password": "666666"},
    {"email": "cpmkingking31@gmail.com", "password": "666666"},
    {"email": "cpmkingking32@gmail.com", "password": "666666"},
    {"email": "cpmkingking33@gmail.com", "password": "666666"},
    {"email": "cpmkingking34@gmail.com", "password": "666666"},
    {"email": "cpmkingking35@gmail.com", "password": "666666"},
    {"email": "cpmkingking36@gmail.com", "password": "666666"},
    {"email": "cpmkingking37@gmail.com", "password": "666666"},
    {"email": "cpmkingking38@gmail.com", "password": "666666"},
    {"email": "cpmkingking39@gmail.com", "password": "666666"},
    {"email": "cpmkingking40@gmail.com", "password": "666666"},
    {"email": "cpmkingking41@gmail.com", "password": "666666"},
    {"email": "cpmkingking42@gmail.com", "password": "666666"},
]

# --- Функции для аккаунтов ---
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
    for acc in ACCOUNTS:
        token = login(acc["email"], acc["password"])
        if token:
            set_rank(token)
    return True

# --- Telegram Handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Запуск KING RANK...")
    run_rank()
    await update.message.reply_text("👑 KING RANK установлены на всех аккаунтах!")

# --- Flask для Render ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()

# --- Telegram Bot ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
