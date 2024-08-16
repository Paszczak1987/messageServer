from tools.menu import Option, Menu
from service import *



def user_service():
    menu = Menu(
            Option("Dodaj użytkownika", add_user),
            Option("Usuń użytkownika", erase_user),
            Option("Edytuj użytkownika", edit_user),
            Option("Pobierz za pomocą id", get_user_by_id),
            Option("Pobierz za pomocą nazwy", get_user_by_username),
            Option("Pobierz wszystkich", get_all_users),
            indent="  "
            )
    menu.start()

menu = Menu( Option('Użytkownicy', user_service))
menu.app_name = "Zarządzanie użytkownikami"
menu.start()



