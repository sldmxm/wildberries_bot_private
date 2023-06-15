from telegram import Update
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard

from telegram.ext import ContextTypes
from bot.constants.text import SUBSCRIBTION_IS_FALSE, SUBSCRIBTION_IS_TRUE
from bot.utils import check_subscription


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора действий в кнопках под текстом."""
    query = update.callback_query
    if query.data == 'check_subscription':
        if await check_subscription(update, context):
            await query.answer('Выполняется проверка подписки на канал.')
            await update.effective_chat.send_message(SUBSCRIBTION_IS_TRUE)
        else:
            await query.answer('Подписка на канал не найдена.')
            keyboard = [
                [
                    Button(
                        'Я подписался, запустить бота',
                        callback_data='check_subscription'
                    )
                ]
            ]
            reply_markup = Keyboard(keyboard)
            await query.message.reply_text(
                SUBSCRIBTION_IS_FALSE,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
