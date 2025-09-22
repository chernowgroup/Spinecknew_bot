import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== הכנס כאן את הטוקן שלך מטלגרם ======
os.environ["TOKEN"]
# ====== רשימת החלפות מילים בעייתיות ======
REPLACEMENTS = {
    "medical": "wellness",
    "therapy": "relaxation",
    "therapeutic": "soothing",
    "doctor": "trusted",
    "cure": "helps relieve",
    "heal": "supports recovery",
    "fix": "improves",
    "prevent": "reduces risk of",
    "guarantee": "encourages",
    "instantly": "quickly",
    "painkiller": "massage support",
    "clinical": "home-friendly"
}

def clean_text(text: str) -> dict:
    found = []
    new_text = text
    for bad, good in REPLACEMENTS.items():
        if bad.lower() in new_text.lower():
            found.append((bad, good))
            new_text = new_text.replace(bad, good).replace(bad.capitalize(), good.capitalize())
    return {"original": text, "cleaned": new_text, "replacements": found}

# ===== פקודה /check =====
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    title = "6-Head Deep Tissue Massage Gun – Therapy for Muscle Pain Relief"
    description = "This medical massage device is doctor approved. It guarantees to cure sore muscles and fix stiffness instantly."

    result_title = clean_text(title)
    result_desc = clean_text(description)

    bad_words = result_title["replacements"] + result_desc["replacements"]
    replaced = "\n".join([f"❌ {b} → ✅ {g}" for b, g in bad_words])

    message = (
        f"🚨 מילים בעייתיות זוהו:\n{replaced if replaced else 'אין'}\n\n"
        f"📌 גרסה מתוקנת:\n"
        f"*Title:* {result_title['cleaned']}\n"
        f"*Description:* {result_desc['cleaned']}"
    )

    keyboard = [
        [
            InlineKeyboardButton("✔ אשר", callback_data="approve"),
            InlineKeyboardButton("✖ שמור מקור", callback_data="reject"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# ===== טיפול בכפתורים =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "approve":
        await query.edit_message_text("✅ אושר! הטקסט המתוקן יעלה לפרסום.")
    elif query.data == "reject":
        await query.edit_message_text("❌ נשמר המקור. המודעה תעלה כמו שהיא (ייתכן שתיפסל).")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
