import logging
from telegram import Update
from telegram.ext import ContextTypes
from plugins import plugin_manager

class MessageReader:
    
    def __init__(self):
        self.plugin_manager = plugin_manager
    
    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_message or not update.effective_chat:
            return
        
        if update.effective_chat.type not in ['group', 'supergroup']:
            return
        
        await self.plugin_manager.process_message(update, context)
    
    async def process_status_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_chat:
            return
        
        if update.effective_chat.type not in ['group', 'supergroup']:
            return
        
        await self.plugin_manager.process_status_update(update, context)
    
    async def process_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.plugin_manager.process_callback(update, context)