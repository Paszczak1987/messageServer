from tools.menu import Option, Menu, MenuArgs
from serviceArgs import *


def user_service():
    options = {
        "-add": Option("Dodaj użytkownika", add_user, "<nazwa_użytkownika> <hasło>"),
        "-rm_i": Option("Usuń użytkownika", erase_user_i, "<id>"),
        "-rm_n": Option("Usuń użytkownika", erase_user_n, "<nazwa_użytkownika>"),
        "-ed": Option("Edytuj użytkownika", edit_user, "<id> <nazwa_użytkownika> <hasło>"),
        "-get_i": Option("Wczytaj uż. po id", show_user_by_id, "<id>"),
        "-get_n": Option("Wczytaj uż. po nazwie", show_user_by_name, "<nazwa_użytkownika>"),
        "-get": Option("Wczytaj wszystkich uż.", show_all_users)
        }
    menu = MenuArgs(options, indent="  ")
    menu.start()
    
menu = Menu(Option("Zarządzaj", user_service))
menu.app_name = "Zarządzanie użytkownikami"
menu.start()
