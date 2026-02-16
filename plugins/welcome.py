import logging
from telegram import Update
from telegram.ext import ContextTypes
from lib.handler import MessageHandler

class WelcomePlugin:
    
    WELCOME_TEXT = """
<i><b>ᴡᴇʟᴄᴏᴍᴇ, </b></i><a href="tg://user?id={user_id}">{first_name}</a>, 

<i>ᴡᴇ ᴀʀᴇ ɴᴏᴡ ᴛᴏᴛᴀʟ {members_count} ᴍᴇᴍʙᴇʀ'ꜱ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</i>
    """
    
    async def handle_status_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        chat = update.effective_chat
        
        if not message or not message.new_chat_members:
            return
        
        for new_member in message.new_chat_members:
            if new_member.id == context.bot.id:
                continue
            
            await self.welcome_member(update, context, new_member)
    
    async def welcome_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE, new_member):
        chat = update.effective_chat
        
        try:
            member_count = await chat.get_member_count()
        except:
            member_count = 0
        
        welcome_text = self.WELCOME_TEXT.format(
            user_id=new_member.id,
            first_name=new_member.first_name,
            members_count=member_count
        )
        
        await context.bot.send_message(
            chat_id=chat.id,
            text=welcome_text,
            parse_mode='HTML'
        )
        
        logging.info(f"Welcome message sent for {new_member.first_name} in {chat.id}")