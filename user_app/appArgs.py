from tools.menu import Option,Menu, MenuArgs
from serviceArgs import add_user, erase_user_i, erase_user_n, edit_user, get_user_by_id, get_user_by_username, get_all_users


def user_service():
    options = {
        "-add": Option("Dodaj użytkownika", add_user, "<nazwa_użytkownika> <hasło>"),
        "-rm_i": Option("Usuń użytkownika", erase_user_i, "<id>"),
        "-rm_n": Option("Usuń użytkownika", erase_user_n, "<nazwa_użytkownika>"),
        "-ed": Option("Edytuj użytkownika", edit_user, "<id> <nazwa_użytkownika> <hasło>"),
        "-get_i": Option("Wczytaj uż. po id", get_user_by_id, "<id>"),
        "-get_n": Option("Wczytaj uż. po nazwie", get_user_by_username, "<nazwa_użytkownika>"),
        "-get": Option("Wczytaj wszystkich uż.", get_all_users)
        }
    menu = MenuArgs(options, indent="  ")
    menu.start()
    
menu = Menu(Option("Zarządzaj", user_service))
menu.app_name = "Zarządzanie użytkownikami"
menu.start()
