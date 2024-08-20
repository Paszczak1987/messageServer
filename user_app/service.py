from tools.models import User

def add_user():
    username = input("Username: ")
    password = input("Password: ")
    user = User(username, password)
    user.save()

def erase_user():
    id = int(input("Enter user ID: "))
    user = User.get_by_id(id)
    user.remove()

def edit_user():
    id = int(input('Podaj id: '))
    username = input('Nazwa użytkownika: ')
    password = input('Hasło: ')
    user = User.get_by_id(id)
    user.update(username, password)

def get_user_by_id():
    user_id = int(input('Podaj id użytkownika: '))
    return User.get_by_id(user_id)

def get_user_by_username():
    username = input("Podaj nazwę użytkownika: ")
    print(User.get_by_name(username))

def get_all_users():
    users = User.get_all()
    for user in users:
        print(user)