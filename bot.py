from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello 👋\n\n"
        "Send me any message and I will answer using AI.\n"
        "Use /image <description> to generate images."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": update.message.text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Use: /image a cat in space")
        return

    img = openai.Image.create(prompt=prompt, size="1024x1024")
    await update.message.reply_photo(img["data"][0]["url"])

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("image", image))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot is running...")
app.run_polling()
