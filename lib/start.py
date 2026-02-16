from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from lib.config import Config
from lib.handler import MessageHandler

START_TEXT = """
<i><b>ʜᴇʟʟᴏ, </b></i><a href="tg://user?id={user_id}">{first_name}</a><i>! <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀᴅᴠᴀɴᴄᴇ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ...</b>

ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ ꜰʀᴏᴍ ᴜɴᴡᴀɴᴛᴇᴅ ʟɪɴᴋ'ꜱ ᴀɴᴅ ʙᴏᴛ ᴍᴇɴᴛɪᴏɴ'ꜱ
ꜱᴇʟᴇᴄᴛ ʜᴇʟᴘ ꜰʀᴏᴍ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴍᴏʀᴇ ɪɴꜰᴏ</i>
"""

class StartHandler:
    @staticmethod
    def main_menu():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/dokaebiiii"),
                InlineKeyboardButton("ʜᴇʟᴘ/ɢᴜɪᴅᴇ", callback_data="help")
            ],
            [InlineKeyboardButton(
                "ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ", 
                url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
            )]
        ])
    
    @staticmethod
    def back_button():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("« ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ", callback_data="main_menu")]
        ])
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        context.user_data.clear()
        
        formatted_text = START_TEXT.format(
            user_id=user.id,
            first_name=user.first_name
        )
        
        await MessageHandler.send_text(
            context,
            update.effective_chat.id,
            formatted_text,
            reply_markup=self.main_menu()
        )
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        
        if query.data == "main_menu":
            await query.edit_message_text(
                START_TEXT.format(user_id=user.id, first_name=user.first_name),
                parse_mode=ParseMode.HTML,
                reply_markup=self.main_menu()
            )
        elif query.data == "help":
            from lib.help import HELP_TEXT
            await query.edit_message_text(
                HELP_TEXT.format(user_id=user.id, first_name=user.first_name),
                parse_mode=ParseMode.HTML,
                reply_markup=self.back_button()
            )