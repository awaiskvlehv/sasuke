import logging
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

class MessageHandler:
    
    @staticmethod
    async def send_text(
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        text: str,
        reply_markup: InlineKeyboardMarkup = None,
        reply_to_message_id: int = None,
        parse_mode: str = ParseMode.HTML
    ):
        try:
            return await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id
            )
        except Exception as e:
            logging.error(f"Failed to send text: {e}")
            return None
    
    @staticmethod
    async def send_photo(
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        photo: str,
        caption: str = None,
        reply_markup: InlineKeyboardMarkup = None,
        reply_to_message_id: int = None,
        parse_mode: str = ParseMode.HTML
    ):
        try:
            return await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id
            )
        except Exception as e:
            logging.error(f"Failed to send photo: {e}")
            if caption:
                return await MessageHandler.send_text(
                    context, chat_id, caption, reply_markup, reply_to_message_id, parse_mode
                )
            return None
    
    @staticmethod
    async def send_sticker(
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        sticker: str,
        reply_to_message_id: int = None
    ):
        try:
            return await context.bot.send_sticker(
                chat_id=chat_id,
                sticker=sticker,
                reply_to_message_id=reply_to_message_id
            )
        except Exception as e:
            logging.error(f"Failed to send sticker: {e}")
            return None
    
    @staticmethod
    async def delete_message(
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        message_id: int
    ):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            return True
        except Exception as e:
            logging.error(f"Failed to delete message: {e}")
            return False
    
    @staticmethod
    def create_mention(user):
        name = user.first_name or "Friend"
        return f"<a href='tg://user?id={user.id}'>{name}</a>"