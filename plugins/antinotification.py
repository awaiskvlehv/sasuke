#!/usr/bin/env python3
"""
Anti-Notifications Plugin - Delete all system notifications
Deletes: join, leave, group photo change, group title change, etc.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from lib.handler import MessageHandler

class AntiNotificationsPlugin:
    """Deletes all system notifications from groups"""
    
    async def handle_status_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Delete all status update messages"""
        message = update.effective_message
        chat = update.effective_chat
        
        if not message:
            return
        
        # Check if bot is admin
        try:
            bot_member = await chat.get_member(context.bot.id)
            if bot_member.status not in ['administrator', 'creator']:
                return
        except:
            return
        
        # Types of messages to delete:
        should_delete = False
        
        # New chat members (join)
        if message.new_chat_members:
            # Don't delete if bot itself joined
            for member in message.new_chat_members:
                if member.id == context.bot.id:
                    return
            should_delete = True
        
        # Left chat member (leave)
        elif message.left_chat_member:
            # Don't delete if bot itself left
            if message.left_chat_member.id == context.bot.id:
                return
            should_delete = True
        
        # Group photo changes
        elif message.group_chat_created or message.supergroup_chat_created:
            should_delete = True
        elif message.delete_chat_photo or message.new_chat_photo:
            should_delete = True
        
        # Group title changes
        elif message.new_chat_title:
            should_delete = True
        
        # Pinned messages
        elif message.pinned_message:
            should_delete = True
        
        # Video chat started/ended
        elif message.video_chat_started or message.video_chat_ended:
            should_delete = True
        elif message.video_chat_participants_invited:
            should_delete = True
        
        # Message auto-delete timer changed
        elif message.message_auto_delete_timer_changed:
            should_delete = True
        
        # Migrate from group to supergroup
        elif message.migrate_from_chat_id or message.migrate_to_chat_id:
            should_delete = True
        
        # Connected website
        elif message.connected_website:
            should_delete = True
        
        # Delete if matches any condition
        if should_delete:
            await MessageHandler.delete_message(context, chat.id, message.message_id)
            logging.info(f"Deleted notification in chat {chat.id}")