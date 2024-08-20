from tools.models import User, Message

def check_messages(user):
    return Message.get_all_user_msgs(user._id)
    