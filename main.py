# main.py
import logging
import sys
import os
import requests
import importlib
import inspect
import threading
import time
from pathlib import Path

# ==================== CONFIG ====================
BOT_TOKEN = "8472097020:AAG5YrJ7infB569Uq5B94leRd6LFTLUEnp8"
GITHUB_REPO = "awaiskvlehv/sasuke"
GITHUB_BRANCH = "main"
SYNC_INTERVAL = 60

# ==================== GITHUB LOADER ====================
class GitHubLoader:
    def __init__(self):
        self.base_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
        self.modules = {}
        self.last_check = 0
        
    def fetch(self, path):
        try:
            url = f"{self.base_url}/{path}?ref={GITHUB_BRANCH}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except: pass
        return []
    
    def download(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except: pass
        return None
    
    def load_module(self, name, code):
        try:
            spec = importlib.util.spec_from_loader(name, loader=None)
            module = importlib.util.module_from_spec(spec)
            exec(code, module.__dict__)
            sys.modules[name] = module
            return module
        except: return None

# ==================== MAIN LOADER ====================
class BotLoader:
    def __init__(self):
        self.github = GitHubLoader()
        self.application = None
        self.plugin_manager = None
        self.running = True
        
    def install_dependencies(self):
        """Auto install requirements"""
        try:
            req_file = self.github.download(
                f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/requirements.txt"
            )
            if req_file:
                for line in req_file.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        os.system(f"pip install {line}")
                        print(f"✅ Installed: {line}")
        except: pass
    
    def load_lib_files(self):
        """Load all lib files from GitHub"""
        lib_files = self.github.fetch("lib")
        for file in lib_files:
            if file['name'].endswith('.py'):
                code = self.github.download(file['download_url'])
                if code:
                    module_name = f"lib.{file['name'][:-3]}"
                    self.github.load_module(module_name, code)
                    print(f"📚 Loaded lib: {file['name']}")
    
    def load_plugins(self):
        """Load plugins from GitHub"""
        # First load plugins/__init__.py
        init_file = self.github.fetch("plugins/__init__.py")
        if init_file and isinstance(init_file, dict) and init_file.get('type') == 'file':
            code = self.github.download(init_file['download_url'])
            if code:
                module = self.github.load_module("plugins", code)
                if module and hasattr(module, 'plugin_manager'):
                    self.plugin_manager = module.plugin_manager
                    print("✅ Plugin manager loaded")
        
        # Then load all plugin files
        plugin_files = self.github.fetch("plugins")
        for file in plugin_files:
            if file['name'].endswith('.py') and file['name'] != '__init__.py':
                code = self.github.download(file['download_url'])
                if code:
                    module_name = f"plugins.{file['name'][:-3]}"
                    self.github.load_module(module_name, code)
                    print(f"🔌 Loaded plugin: {file['name']}")
    
    def auto_sync(self):
        """Auto sync thread"""
        def sync_loop():
            while self.running:
                try:
                    print("🔄 Checking for updates...")
                    self.load_plugins()
                except: pass
                time.sleep(SYNC_INTERVAL)
        
        thread = threading.Thread(target=sync_loop, daemon=True)
        thread.start()
    
    def run(self):
        print("\n" + "="*50)
        print("🚀 BOT LOADER STARTING...")
        print("="*50)
        
        # Step 1: Install dependencies
        print("\n📦 Installing dependencies...")
        self.install_dependencies()
        
        # Step 2: Import telegram
        global Application, Update, CommandHandler, MessageHandler, filters, CallbackQueryHandler
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
        
        # Step 3: Load lib files
        print("\n📚 Loading lib files...")
        self.load_lib_files()
        
        # Step 4: Load plugins
        print("\n🔌 Loading plugins...")
        self.load_plugins()
        
        # Step 5: Start auto sync
        self.auto_sync()
        
        # Step 6: Create application
        print("\n🤖 Starting bot...")
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Step 7: Setup handlers from plugin manager
        if self.plugin_manager:
            # Message handler
            self.application.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.plugin_manager.process_message
            ))
            
            # Status update handler
            self.application.add_handler(MessageHandler(
                filters.StatusUpdate.ALL,
                self.plugin_manager.process_status_update
            ))
            
            # Callback handler
            self.application.add_handler(CallbackQueryHandler(
                self.plugin_manager.process_callback
            ))
            
            # Command handlers from lib
            if 'lib.start' in sys.modules:
                self.application.add_handler(CommandHandler("start", sys.modules['lib.start'].StartHandler().start_command))
                self.application.add_handler(CallbackQueryHandler(sys.modules['lib.start'].StartHandler().callback_handler))
            
            if 'lib.help' in sys.modules:
                self.application.add_handler(CommandHandler("help", sys.modules['lib.help'].HelpHandler().help_command))
        
        # Step 8: Error handler
        async def error_handler(update, context):
            logging.error(f"Error: {context.error}")
        self.application.add_error_handler(error_handler)
        
        # Step 9: Print status
        print("\n" + "="*50)
        print("✅ BOT IS RUNNING!")
        print(f"📊 Plugins loaded: {len(self.plugin_manager.plugins) if self.plugin_manager else 0}")
        print("🔄 Auto-sync active (60s)")
        print("="*50 + "\n")
        
        # Step 10: Start polling
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== START ====================
if __name__ == "__main__":
    loader = BotLoader()
    try:
        loader.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped!")
        loader.running = False