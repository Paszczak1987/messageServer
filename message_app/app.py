from tools.menu import Option, Menu
from service import *

app_name = "Aplikacja do wysyłania wiadomości"

def user_service():
    login_data = login()
    if login_data["login_ok"]:
        user = login_data["user"]
        menu = Menu(
                Option("Odbierz wiadomości", receive_messages),
                Option("Zobacz wysłane", get_all_sent),
                Option("Wyślij", send_msg),
                Option("Usuń", remove_msg),
                indent="  "
                )
        menu.user = user
        menu.start()


menu = Menu(Option('Logowanie', user_service))
menu.app_name = app_name
menu.start()
