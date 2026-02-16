from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from lib.handler import MessageHandler

HELP_TEXT = """
<i><b>ʜᴇʟʟᴏ, </b></i><a href="tg://user?id={user_id}">{first_name}</a><i>! <b>ɪ'ᴍ ꜱᴀꜱᴜᴋᴇ ᴜᴄʜɪʜᴀ...</b>

ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ʙᴏᴛ ᴛᴏ ᴍᴀɴᴀɢᴇ ɢʀᴏᴜᴘ'ꜱ ᴡɪᴛʜ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ'ꜱ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇ ꜰᴇᴀᴛᴜʀᴇ'ꜱ
ʀᴇᴀᴅ ʙᴇʟᴏᴡ ᴍʏ ꜰᴇᴀᴛᴜʀᴇ'ꜱ...

<b>ꜰᴇᴀᴛᴜʀᴇ'ꜱ :</b>
• ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴜʀʟꜱ/ʟɪɴᴋꜱ
• ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ʙᴏᴛ ᴜꜱᴇʀɴᴀᴍᴇꜱ  
• ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴍᴇɴᴛɪᴏɴꜱ
• ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ᴘɪᴄᴛᴜʀᴇ
• ɢᴏᴏᴅʙʏᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ᴘɪᴄᴛᴜʀᴇ
• ɢᴍ/ɢɴ ɢʀᴇᴇᴛɪɴɢ ʀᴇᴘʟɪᴇꜱ ᴡɪᴛʜ ꜱᴛɪᴄᴋᴇʀꜱ
• ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴊᴏɪɴ/ʟᴇᴀᴠᴇ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴꜱ

<b>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ?</b>
1. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
2. ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ
3. ɢɪᴠᴇ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ

<b>ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> @dokaebiiii
</i>
"""

class HelpHandler:
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        formatted_text = HELP_TEXT.format(
            user_id=user.id,
            first_name=user.first_name
        )
        
        from lib.start import StartHandler
        await MessageHandler.send_text(
            context,
            update.effective_chat.id,
            formatted_text,
            reply_markup=StartHandler.back_button()
        )