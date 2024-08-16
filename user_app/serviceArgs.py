from tools.models import User

def add_user(args=None):
    if args:
        if len(args) == 2:
            user = User(args[0], args[1])
            user.save()
            print(f"Dodano {user.username} id {user._id}.")
        else:
            print("Niepoprawne dane")
    else:
        print("Nie podano argumentów.")


def erase_user_i(args):
    id = int(args[0])
    id_list = User.get_ids()
    if id in id_list:
        user = User.get_user_by_id(id)
        user.remove()
        print(f"Usunięto: id:{user._id} - {user.username}")
    else:
        print(f"Użytkownik o id {id} nie istnieje")


def erase_user_n(args):
    names = User.get_names()
    if args[0] in names:
        user = User.get_user_by_name(args[0])
        user.remove()
        print(f"Usunięto: id:{user._id} - {user.username}")
    else:
        print(f"Użytkownik {args[0]} nie istnieje.")


def edit_user(args):
    id = int(args[0])
    id_list = User.get_ids()
    if id in id_list:
        user = User.get_user_by_id(id)
        user.update(args[1], args[2])
        print(f"Edycja udana.")
    else:
        print(f"Użytkownik o id {id} nie istnieje.")


def get_user_by_id(args):
    id = int(args[0])
    id_list = User.get_ids()
    if id in id_list:
        print(User.get_user_by_id(id))
    else:
        print(f"Użytkownik o id {id} nie istnieje.")


def get_user_by_username(args):
    names = User.get_names()
    if args[0] in names:
        print(User.get_user_by_name(args[0]))
    else:
        print(f"Użytkownik {args[0]} nie istnieje.")


def get_all_users():
    users = User.get_all_users()
    for user in users:
        print(user)
        
        