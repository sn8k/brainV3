import logging
import importlib
import os

class PluginGateway:
    def __init__(self, plugins):
        self.plugins = plugins

    def load_plugins(self):
        for plugin in self.plugins:
            plugin_name = plugin.__name__
            logging.info("Plugin loaded in PluginGateway: %s", plugin_name)

    def run_background_tasks(self):
        self.load_plugins()
        for plugin in self.plugins:
            if hasattr(plugin, 'execute'):
                plugin_thread = threading.Thread(target=plugin.execute)
                plugin_thread.start()
