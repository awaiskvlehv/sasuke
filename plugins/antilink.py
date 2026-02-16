import re
import logging
from telegram import Update
from telegram.ext import ContextTypes
from lib.handler import MessageHandler

class URLPatternDetector:
    
    @staticmethod
    def create_advanced_pattern():
 
        protocol = r'(?:(?:https?|ftp|sftp|ftps|ssh|git|svn|ws|wss):\/\/)'
        auth = r'(?:[a-zA-Z0-9\-_]+(?::[a-zA-Z0-9\-_]+)?@)?'
        
        ipv4 = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        ipv6 = r'\[(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]'
        
        domain = r'(?:[a-zA-Z0-9\u00a1-\uffff][a-zA-Z0-9\u00a1-\uffff_-]{0,62})'
        tld = r'\.[a-zA-Z\u00a1-\uffff]{2,}'
        full_domain = r'(?:' + domain + r'(?:\.' + domain + r')*' + tld + r')'
        
        host = r'(?:' + ipv4 + r'|' + ipv6 + r'|' + full_domain + r')'
        
        port = r'(?::\d{2,5})?'
        
        path = r'(?:/[^\s?#]*)?'
        query = r'(?:\?[^\s#]*)?'
        fragment = r'(?:#[^\s]*)?'
        
        url_pattern = protocol + auth + host + port + path + query + fragment
        
        www_pattern = r'www\.' + full_domain + path + query + fragment
        
        telegram_pattern = r'(?:t(?:elegram)?)\.(?:me|dog)/(?!channel/|addstickers/|addemoji/)[a-zA-Z0-9_]+(?:/[a-zA-Z0-9_]+)?'
        
        # Remove social_pattern from here since it captures @mentions
        short_url_pattern = r'(?:bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|short\.to)/[a-zA-Z0-9\-_]+'
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        discord_pattern = r'(?:discord(?:app)?\.com/invite|discord\.gg)/[a-zA-Z0-9\-_]+'
        
        github_pattern = r'github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+(?:/blob/[^/\s]+/[^\s]*|/tree/[^/\s]+/[^\s]*|/pull/\d+|/issues/\d+)?'
        
        fileshare_pattern = r'(?:drive\.google\.com/(?:file/d/|open\?id=)|dropbox\.com/scl/fi|mega\.nz/(?:file|folder)|mediafire\.com/file|wetransfer\.com/downloads)/[a-zA-Z0-9\-_]+'
        
        invite_pattern = r't\.me/(?:joinchat/|\+)[a-zA-Z0-9_-]+'
        
        full_pattern = r'(?:' + '|'.join([
            url_pattern,
            www_pattern,
            telegram_pattern,
            short_url_pattern,
            discord_pattern,
            github_pattern,
            fileshare_pattern,
            email_pattern,
            invite_pattern  # Added invite_pattern here
        ]) + r')'
        
        return re.compile(full_pattern, re.IGNORECASE)
    
    _pattern = create_advanced_pattern.__func__()
    
    @classmethod
    def is_url(cls, text):
        if not text:
            return False
        return bool(cls._pattern.search(text))
    
    @classmethod
    def extract_urls(cls, text):
        if not text:
            return []
        return cls._pattern.findall(text)


class AntiLinkPlugin:

    WARNING_MESSAGE = """
<i>hey, </i><a href="tg://user?id={user_id}">{first_name}</a>, 

<i>Your message was deleted because it {reason}.</i>
    """
    
    REASON_TYPES = {
        "url": "contains a <b>link</b>",
        "bot": "mentions a <b>bot</b>",
        "gc": "mentions a <b>group, channel or user</b>"
    }
    
    @staticmethod
    def is_url(text):
        return URLPatternDetector.is_url(text)
    
    @staticmethod
    def is_bot_mention(text):
        # Pattern for bot mentions (usernames ending with 'bot')
        bot_pattern = re.compile(r'@(\w+bot)\b', re.IGNORECASE)
        # Also check for t.me/botname pattern
        tme_bot_pattern = re.compile(r't\.me/(\w+bot)(?:/)?\b', re.IGNORECASE)
        return bool(bot_pattern.search(text)) or bool(tme_bot_pattern.search(text))
    
    @staticmethod
    def is_group_channel_mention(text):
        # First, extract all @mentions
        mention_pattern = re.compile(r'@(\w+)\b')
        mentions = mention_pattern.findall(text)
        
        # Check each mention - if it's not a bot, it's a group/channel/user mention
        for mention in mentions:
            if not mention.lower().endswith('bot'):
                return True
        
        # Check for Telegram invite links (these are group/channel invites)
        invite_pattern = re.compile(r't\.me/(?:joinchat/|\+)[a-zA-Z0-9_-]+')
        if invite_pattern.search(text):
            return True
            
        # Check for t.me/username links that are NOT bots
        tme_pattern = re.compile(r't\.me/([a-zA-Z0-9_]+)(?:/)?\b')
        tme_matches = tme_pattern.findall(text)
        for match in tme_matches:
            if not match.lower().endswith('bot') and not match.startswith('joinchat') and match != '+':
                return True
        
        return False
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        chat = update.effective_chat
        user = update.effective_user
        
        if not message or not message.text:
            return
        
        # Check if user is admin
        try:
            chat_member = await chat.get_member(user.id)
            if chat_member.status in ['administrator', 'creator']:
                return
        except:
            pass
        
        # Check if bot is admin
        try:
            bot_member = await chat.get_member(context.bot.id)
            if bot_member.status not in ['administrator', 'creator']:
                return
        except:
            return
        
        text = message.text
        delete_reason = None
        
        # Check for bot mentions first (more specific)
        if self.is_bot_mention(text):
            delete_reason = "bot"
        # Then check for group/channel mentions
        elif self.is_group_channel_mention(text):
            delete_reason = "gc"
        # Finally check for URLs (now won't catch @mentions)
        elif self.is_url(text):
            delete_reason = "url"
        
        if delete_reason:
            await MessageHandler.delete_message(context, chat.id, message.message_id)
            await self.send_warning(update, context, delete_reason)
    
    async def send_warning(self, update: Update, context: ContextTypes.DEFAULT_TYPE, reason: str):
        user = update.effective_user
        chat = update.effective_chat
        
        reason_text = self.REASON_TYPES.get(reason, "contains prohibited content")
        
        formatted_text = self.WARNING_MESSAGE.format(
            user_id=user.id,
            first_name=user.first_name,
            reason=reason_text
        )
        
        await context.bot.send_message(
            chat_id=chat.id,
            text=formatted_text,
            parse_mode='HTML'
        )