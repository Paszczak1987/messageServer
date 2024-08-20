from tools.models import User

users = User.get_all_users()

for user in users:
    print(user._id, user.username, user._hashed_password)

