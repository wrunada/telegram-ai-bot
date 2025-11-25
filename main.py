import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from huggingface_hub import InferenceClient
import io

TELEGRAM_TOKEN = "6822418340:AAHPQN8cx-EfkReSJhHifnqlgmoQCbC7CYE"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
client = InferenceClient(token=HF_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku bot AI canggih!\nKetik apa saja → aku jawab pake Gemini AI\n/gambar [teks] → aku buatin gambar")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.reply_chat_action("typing")
    response = model.generate_content(msg)
    await update.message.reply_text(response.text or "Hmm, aku bingung nih jawabnya… coba tanya lagi ya")

async def gambar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /gambar kucing pakai topi koboi")
        return
    prompt = " ".join(context.args)
    await update.message.reply_chat_action("upload_photo")
    image = client.text_to_image(prompt)
    bio = io.BytesIO(image)
    bio.seek(0)
    await update.message.reply_photo(bio, caption=f"{prompt}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gambar", gambar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
