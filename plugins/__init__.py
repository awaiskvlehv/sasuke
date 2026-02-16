import logging
import importlib
import pkgutil
from pathlib import Path

class PluginManager:
    def __init__(self):
        self.plugins = []
        self.load_plugins()
    
    def load_plugins(self):
        plugins_dir = Path(__file__).parent
        for module_info in pkgutil.iter_modules([str(plugins_dir)]):
            if module_info.name == "__init__":
                continue
            try:
                module = importlib.import_module(f"plugins.{module_info.name}")
                for attr_name in dir(module):
                    if attr_name.endswith("Plugin") and attr_name != "Plugin":
                        plugin_class = getattr(module, attr_name)
                        self.plugins.append(plugin_class())
                        logging.info(f"✅ Loaded plugin: {module_info.name}")
                        break
            except Exception as e:
                logging.error(f"❌ Failed to load plugin {module_info.name}: {e}")
    
    async def process_message(self, update, context):
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'handle_message'):
                    await plugin.handle_message(update, context)
            except Exception as e:
                logging.error(f"Error in plugin: {e}")
    
    async def process_status_update(self, update, context):
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'handle_status_update'):
                    await plugin.handle_status_update(update, context)
            except Exception as e:
                logging.error(f"Error in plugin: {e}")
    
    async def process_callback(self, update, context):
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'handle_callback'):
                    await plugin.handle_callback(update, context)
            except Exception as e:
                logging.error(f"Error in plugin: {e}")

plugin_manager = PluginManager()
