#!/usr/bin/env python3
"""
Reply Greetings Plugin - Reply to GM/GN messages with stickers
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from lib.handler import MessageHandler

class ReplyGreetsPlugin:
    """Replies to Good Morning/Good Night messages"""
    
    # Plugin configuration
    GN_STICKER = "CAACAgUAAxkBAAEC7B5mvnhFWRh8TVNxGiCuLLwp3Qt4EQACaAYAApgIqFX0lPxGg7S_IDUE"
    GM_STICKER = "CAACAgIAAxkBAAEDKvdoVbAvSxDVpNNdAAHIo1YsjzcKqfkAAmAAA3io5g-XR8l_6mIspB4E"
    
    GOOD_NIGHT = """
<b>❖ ɢᴏᴏᴅ ɴɪɢʜᴛ ❖ sᴡᴇᴇᴛ ᴅʀᴇᴀᴍs ❖

❍  {mention} 😪 

❖ ɢᴏ ᴛᴏ ➥ sʟᴇᴇᴘ ᴇᴀʀʟʏ
</b>"""
    
    GOOD_MORNING = """
<b>❖ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ❖ ʜᴀᴠᴇ ᴀ ɴɪᴄᴇ ᴅᴀʏ ❖

❍  {mention} 🌞 

❖ sᴛᴀʏ ᴘᴏsɪᴛɪᴠᴇ ➥ ᴋᴇᴇᴘ ꜰᴏᴄᴜꜱᴇᴅ
</b>"""
    
    @staticmethod
    def is_greeting(text):
        """Check if message is GM or GN greeting"""
        if not text:
            return None
        
        text_lower = text.lower().strip()
        
        gn_tags = ["gn", "good night", "g.n", "g n", "night", "gnite", "sleep well", "sweet dreams"]
        gm_tags = ["gm", "good morning", "g.m", "g m", "morning", "vgm", "very good morning"]
        
        if text_lower in gn_tags:
            return "gn"
        elif text_lower in gm_tags:
            return "gm"
        
        return None
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process message for greetings"""
        message = update.effective_message
        chat = update.effective_chat
        user = update.effective_user
        
        if not message or not message.text:
            return
        
        # Check if it's a greeting
        greeting_type = self.is_greeting(message.text)
        
        if greeting_type:
            # Create mention
            mention = MessageHandler.create_mention(user)
            
            # Send appropriate response
            if greeting_type == "gn":
                await MessageHandler.send_text(
                    context,
                    chat.id,
                    self.GOOD_NIGHT.format(mention=mention),
                    reply_to_message_id=message.message_id
                )
                await MessageHandler.send_sticker(
                    context,
                    chat.id,
                    self.GN_STICKER,
                    reply_to_message_id=message.message_id
                )
            elif greeting_type == "gm":
                await MessageHandler.send_text(
                    context,
                    chat.id,
                    self.GOOD_MORNING.format(mention=mention),
                    reply_to_message_id=message.message_id
                )
                await MessageHandler.send_sticker(
                    context,
                    chat.id,
                    self.GM_STICKER,
                    reply_to_message_id=message.message_id
                )
            
            logging.info(f"Sent {greeting_type} greeting to {user.id}")