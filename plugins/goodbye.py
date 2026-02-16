import logging
from telegram import Update
from telegram.ext import ContextTypes
from lib.handler import MessageHandler

class GoodbyePlugin:
    
    GOODBYE_TEXT = """
<i><b>ɢᴏᴏᴅ ʙʏᴇ, </b></i><a href="tg://user?id={user_id}">{first_name}</a>, 

<i>ᴡᴇ ᴀʀᴇ ɴᴏᴡ ᴛᴏᴛᴀʟ {members_count} ᴍᴇᴍʙᴇʀ'ꜱ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</i>
    """
    
    async def handle_status_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        chat = update.effective_chat
        
        if not message or not message.left_chat_member:
            return
        
        left_member = message.left_chat_member
        
        if left_member.id == context.bot.id:
            return
        
        await self.goodbye_member(update, context, left_member)
    
    async def goodbye_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE, left_member):
        chat = update.effective_chat
        
        try:
            member_count = await chat.get_member_count()
        except:
            member_count = 0
        
        goodbye_text = self.GOODBYE_TEXT.format(
            user_id=left_member.id,
            first_name=left_member.first_name,
            members_count=member_count
        )
        
        await context.bot.send_message(
            chat_id=chat.id,
            text=goodbye_text,
            parse_mode='HTML'
        )
        
        logging.info(f"Goodbye message sent for {left_member.first_name} in {chat.id}")