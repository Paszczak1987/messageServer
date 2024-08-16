from tools.models import Message, User
from tools.password import check_password
from user_app.service import get_user_by_id


def receive_messages(user):
    messages = Message.get_all_to_user_msgs(user._id)
    for message in messages:
        print(message)

def get_all_sent(user):
    messages = Message.get_all_from_user_msgs(user._id)
    for message in messages:
        print(message)

def send_msg(user):
    print("Do kogo chcesz napisać?")
    for u in User.get_all_users():
        print(u)
    to_whom = get_user_by_id()
    text = input("wiadomość: ")
    msg = Message(user._id, to_whom._id, text)
    msg.send()
    
def remove_msg(user):
    print("Którą wiadomość chcesz usunąć?")
    messages = Message.get_all_user_msgs(user._id)
    ids = [m._id for m in messages]
    for msg in messages: print(msg)
    rm_id = int(input("Podaj id wiadomości: "))
    if rm_id in ids:
        for msg in messages:
            if rm_id == msg._id:
                msg.remove()
                break
    

def login():
    users = [user.username for user in User.get_all_users()]
    username = input('Użytkownik: ')
    ret_val = {
        "login_ok": False,
        "user": None
    }
    if username not in users:
        print(f"Użytkownik {username} nie istnieje.")
        return ret_val
    else:
        user = User.get_user_by_name(username)
        password = input('Hasło: ')
    
        if check_password(password, user._hashed_password):
            print(f"Witaj {username}! ")
            ret_val["login_ok"] = True
            ret_val["user"] = user
            return ret_val
        else:
            print("Niepoprawne hasło.")
            return ret_val
    
       
if __name__ == '__main__':
    login()