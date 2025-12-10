from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import math

# Вставь свой токен
TOKEN = "8425649030:AAEzggVS1tyTvlD8nJ29F_KSqmQUY1HeL5o"


# --------------------------
# ФУНКЦИИ РАСЧЁТА
# --------------------------

def parallax_to_parsec(p_arcsec):
    return 1 / p_arcsec


def cepheid_distance(P_days, m_app, a=-2.76, b=-1.0):
    M = a * math.log10(P_days) + b
    mu = m_app - M
    d_pc = 10 ** ((mu + 5) / 5)
    return d_pc


# --------------------------
# МЕНЮ (ОСНОВНОЕ)
# --------------------------

main_menu = ReplyKeyboardMarkup(
    [
        ["⭐ Параллакс", "🌟 Цефеиды"],
        ["ℹ Помощь", "⌨ Автоввод команд"]
    ],
    resize_keyboard=True
)


# --------------------------
# МЕНЮ ДЛЯ АВТО-ВСТАВКИ КОМАНД
# --------------------------

auto_menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🔭 Ввести параллакс",
            switch_inline_query_current_chat="/parallax "
        )
    ],
    [
        InlineKeyboardButton(
            "🌟 Ввести данные цефеиды",
            switch_inline_query_current_chat="/cepheid "
        )
    ]
])


# --------------------------
# КОМАНДЫ
# --------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Здарова Солнышки! Я бот, который умеет рассчитывать расстояние до звёзд 🔭✨\n\n"
        "📌 *Доступные команды:*\n"
        "• `/parallax <p>` — расстояние по параллаксу (arcsec)\n"
        "• `/cepheid <P> <m>` — расстояние по цефеиде\n"
        "• `/help` — помощь\n\n"
        "Выбери действие с помощью кнопок ниже."
    )
    await update.message.reply_markdown(text, reply_markup=main_menu)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📘 *Помощь*\n\n"
        "Команды:\n"
        "`/parallax <p>` — расстояние по параллаксу\n"
        "`/cepheid <P_days> <m_app>` — расстояние по цефеиде\n"
        "`/start` — главное меню\n\n"
        "Примеры:\n"
        "`/parallax 0.2`\n"
        "`/cepheid 10 5.5`"
    )
    await update.message.reply_markdown(text)


async def parallax_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        p = float(context.args[0])
        d_pc = parallax_to_parsec(p)
        d_ly = d_pc * 3.26156

        await update.message.reply_text(
            f"⭐ Параллакс: {p} arcsec\n"
            f"➡ Расстояние: {d_pc:.2f} pc\n"
            f"➡ {d_ly:.2f} световых лет"
        )
    except:
        await update.message.reply_text(
            "❗ Использование: `/parallax 0.1`",
            parse_mode="Markdown"
        )


async def cepheid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        P = float(context.args[0])
        m = float(context.args[1])
        d_pc = cepheid_distance(P, m)
        d_ly = d_pc * 3.26156

        await update.message.reply_text(
            f"🌟 Цефеида:\n"
            f"Период: {P} дней\n"
            f"Видимая величина: {m}\n\n"
            f"➡ Расстояние: {d_pc:.0f} pc\n"
            f"➡ {d_ly:.0f} световых лет"
        )
    except:
        await update.message.reply_text(
            "❗ Использование: `/cepheid <P_days> <m_app>`\n"
            "Пример: `/cepheid 10 5.5`",
            parse_mode="Markdown"
        )


# --------------------------
# ОБРАБОТЧИК ТЕКСТА
# --------------------------

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "⭐ Параллакс":
        await update.message.reply_text(
            "Введите параллакс, например:\n`/parallax 0.2`",
            parse_mode="Markdown"
        )

    elif msg == "🌟 Цефеиды":
        await update.message.reply_text(
            "Введите период и видимую величину, например:\n`/cepheid 10 5.5`",
            parse_mode="Markdown"
        )

    elif msg == "ℹ Помощь":
        await help_cmd(update, context)

    elif msg == "⌨ Автоввод команд":
        await update.message.reply_text(
            "Выберите команду — она автоматически вставится в поле ввода:",
            reply_markup=auto_menu
        )


# --------------------------
# ЗАПУСК (Python 3.12 SAFE)
# --------------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("parallax", parallax_cmd))
    app.add_handler(CommandHandler("cepheid", cepheid_cmd))

    # Кнопки / текст
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Бот запущен! Открой Telegram и нажми /start")
    app.run_polling()


if __name__ == "__main__":
    main()



