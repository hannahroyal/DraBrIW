import multiprocessing as mp
from multiprocessing.connection import Connection
import os

from DraBrIW.TerminalFrontend import Menu, MenuItem, MenuManager, SubMenu
from DraBrIW.Utils.terminal_utils import int_input


def conn_send_and_print_response(conn: Connection, to_send):
    conn.send(to_send)
    response = conn.recv()
    if response is not None:
        print(response)


class TerminalHandler(mp.Process):
    def __init__(self, conn: Connection):
        super(TerminalHandler, self).__init__()
        self.conn: Connection = conn

        self._init_menu()

    def _init_menu(self):
        self.menu_manager = MenuManager()

        # Set-up Main Menu
        menu_main = Menu("☕ ∆ --- DraBrIW ⍺0.2 --- ∆ ☕", self.menu_manager)
        menu_main.add_item(
            MenuItem("Print database",
                     lambda: conn_send_and_print_response(self.conn, 'print_db'), "Prints the entire database"))
        menu_main.add_item(MenuItem("Help", menu_main.print_help, "Prints this help message"))

        # Set-up Sub Menus
        submenu_order = SubMenu("Order Menu", self.menu_manager)
        submenu_order_single = SubMenu("New Order", self.menu_manager, lambda: self.conn.send("new_single_order"))
        submenu_order_round = SubMenu("New Round", self.menu_manager, lambda: self.conn.send("new_round_order"))

        submenu_order.add_submenu(submenu_order_single)
        submenu_order.add_submenu(submenu_order_round)

        menu_main.add_submenu(submenu_order)

        self.menu_manager.set_main_menu(menu_main)

    def run(self):
        while True:
            self.menu_manager.print_menu()
            choice = int_input("Choice:")

            os.system("clear")

            try:
                self.menu_manager.run_action(choice)
            except ValueError as e:
                print(e)

