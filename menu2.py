import curses
import logging
import json
import importlib

MENU_FILE = './temp_data/menu.lst'

class Menu:
    def __init__(self, stdscr, plugins):
        self.stdscr = stdscr
        self.current_row = 0
        self.plugins = plugins
        self.menus = self.load_menu()
        self.actions = self.initialize_plugin_actions(plugins)
        self.main_menu_options = ["Configuration", "Plugins", "Retour", "Quitter"]

    def load_menu(self):
        try:
            with open(MENU_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("Menu file not found: %s", MENU_FILE)
            return {"main": self.main_menu_options}

    def initialize_plugin_actions(self, plugins):
        actions = {"main": self.main_menu_options}
        for plugin in plugins:
            plugin_name = plugin.__name__.split('.')[-1]
            if hasattr(plugin, 'execute'):
                actions.setdefault("Plugins", {})[plugin_name] = plugin.execute
            if hasattr(plugin, 'configure_plugin'):
                actions.setdefault("Configuration", {})[plugin_name] = plugin.configure_plugin
        return actions

    def print_menu(self, menu_name, selected_row_idx):
        self.stdscr.clear()
        menu = self.menus[menu_name]
        for idx, row in enumerate(menu):
            x = 0
            y = idx
            if idx == selected_row_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def run_action(self, action_name):
        action = self.actions[self.current_menu][action_name]
        if callable(action):
            action(self.stdscr)
        elif isinstance(action, str):
            self.current_menu = action
            self.current_row = 0

    def display(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.current_menu = "main"

        while True:
            self.print_menu(self.current_menu, self.current_row)
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.menus[self.current_menu]) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                action_name = self.menus[self.current_menu][self.current_row]
                if action_name == "Quitter":
                    break
                elif action_name == "Retour":
                    self.current_menu = "main"
                    self.current_row = 0
                else:
                    self.run_action(action_name)

def main_menu_options():
    return ["Configuration", "Plugins", "Retour", "Quitter"]

def main_menu_action():
    pass
