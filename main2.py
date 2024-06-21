import curses
import logging
import importlib.util
import os
import json
from threading import Thread
from plugins.plugin_gateway import PluginGateway

# Configurations
MENU_FILE = './temp_data/menu.lst'
CONFIG_FILE = './config.json'
DEFAULT_CONFIG = {
    'verbosity': 'INFO',
    'required_directories': ['./logs', './data', './temp_data'],
    'plugins_directory': './plugins'
}

# Load configuration
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

# Initialize directories
def initialize_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        else:
            print(f"Directory already exists: {directory}")

# Recreate temp_data directory
def recreate_temp_data_directory():
    temp_data_dir = './temp_data'
    if os.path.exists(temp_data_dir):
        for root, dirs, files in os.walk(temp_data_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(temp_data_dir)
    print(f"Temporary data directory recreated: {temp_data_dir}")

initialize_directories(config['required_directories'])
recreate_temp_data_directory()

# Configure logging
logging.basicConfig(filename='./logs/main2.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Starting project with maximum verbosity")

# Generate menu.lst
def generate_menu_file(plugins):
    menu_data = {
        "Configuration": ["Verbosity"],
        "Plugins": []
    }
    for plugin in plugins:
        plugin_name = plugin.__name__.split('.')[-1]
        menu_data["Plugins"].append({plugin_name: f"{plugin.__name__}.execute"})
    with open(MENU_FILE, 'w') as f:
        json.dump(menu_data, f, indent=4)
    logging.info("Menu list generated")

# Load plugins
def load_plugins():
    plugins = []
    for filename in os.listdir(config['plugins_directory']):
        if filename.endswith('.py') and filename != 'plugin_gateway.py':
            module_name = f"{config['plugins_directory'].replace('/', '.')}.{filename[:-3]}"
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(config['plugins_directory'], filename))
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            plugins.append(plugin_module)
    return plugins

# Start the debug plugin server in a separate thread
def start_debug_plugin():
    try:
        from plugins.debug_plugin import app
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error("Failed to start debug plugin: %s", e)

debug_thread = Thread(target=start_debug_plugin, daemon=True)
debug_thread.start()

# Load and start the plugin gateway in a separate thread
plugins = load_plugins()
plugin_gateway = PluginGateway(plugins)
plugin_gateway_thread = Thread(target=plugin_gateway.run_background_tasks, daemon=True)
plugin_gateway_thread.start()

# Generate menu.lst
generate_menu_file(plugins)

# Start menu
def start_menu(stdscr, plugins):
    from menu2 import Menu
    menu_obj = Menu(stdscr, plugins)
    menu_obj.display()

def main():
    curses.wrapper(start_menu, plugins)

if __name__ == "__main__":
    main()
