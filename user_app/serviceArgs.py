from tools.models import User

def _check_args(n=0, args=None, numeric=False):
    is_ok = False
    if args:
        if len(args) == n and args[0] != '':
             is_ok = True if not numeric else args[0].isnumeric()
    print("Błędne dane.\n" if not is_ok else "", end='')
    return is_ok

def add_user(args=None):
    if _check_args(2, args):
        user = User(args[0], args[1])
        user.save()
        print(f"Dodano {user.username} id {user._id}.")

def erase_user_i(args=None):
    if not _check_args(1, args, True):
        return
    user_id = int(args[0])
    if user_id in User.get_ids():
        user = User.get_user_by_id(user_id)
        user.remove()
        print(f"Usunięto: id:{user._id} - {user.username}")
    else:
        print(f"Użytkownik o id {user_id} nie istnieje")

def erase_user_n(args=None):
    if not _check_args(1, args):
        return
    if args[0] in User.get_names():
        user = User.get_user_by_name(args[0])
        user.remove()
        print(f"Usunięto: id:{user._id} - {user.username}")
    else:
        print(f"Użytkownik {args[0]} nie istnieje.")

def edit_user(args=None):
    if not _check_args(3, args, True):
        return
    user_id = int(args[0])
    if user_id in User.get_ids():
        user = User.get_user_by_id(user_id)
        user.update(args[1], args[2])
        print(f"Edycja udana.")
    else:
        print(f"Użytkownik o id {user_id} nie istnieje.")

def show_user_by_id(args=None):
    if not _check_args(1, args, True):
        return
    user_id = int(args[0])
    if user_id in User.get_ids():
        print(User.get_user_by_id(user_id))
    else:
        print(f"Użytkownik o id {user_id} nie istnieje.")

def show_user_by_name(args=None):
    if not _check_args(1, args):
        return
    if args[0] in User.get_names():
        print(User.get_user_by_name(args[0]))
    else:
        print(f"Użytkownik {args[0]} nie istnieje.")

def show_all_users():
    users = User.get_all_users()
    for user in users:
        print(user)
