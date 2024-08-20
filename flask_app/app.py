from flask import Flask, render_template, request, redirect
from tools.models import User, Message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/user_manager')
def user_manager():
    users = [(user, len(Message.get_all_user_msgs(user._id))) for user in User.get_all_users()]
    return render_template('users.html', users=users)

@app.route('/remove_user', methods=['POST'])
def remove_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        permission = request.form['permission']
        message = None
        user = User.get_user_by_id(int(user_id))
        if permission == 'yes':
            message = f"Użytkownik {user.username} (id:{user_id}) został usunięty."
            if request.form['has_msgs'] == 'yes':
                for msg in Message.get_all_user_msgs(user._id):
                    msg.remove()
                user.remove()
        elif permission == 'no':
            message = f"Użytkownik {user.username} (id:{user_id}) Nie został usunięty."
        return render_template('rm_edit_add_msg.html', message=message)

@app.route('/rm_ask', methods=['POST'])
def rm_ask():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = User.get_user_by_id(int(user_id))
        return render_template('rm_ask.html', user=user)

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        user = User.get_user_by_id(user_id)
        user.update(request.form['username'], request.form['password'])
        message = f"Użytkownik o id:{user_id} został zaktualizowany."
        return render_template('rm_edit_add_msg.html', message=message)
    else:
        user_id = int(request.args.get('user_id'))
        user = User.get_user_by_id(user_id)
        return render_template('edit_user.html', user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user = User(name, password)
        user.save()
        message = f"Dodano użytkownika {user.username} (id:{user._id})"
        return render_template('rm_edit_add_msg.html', message=message)
    else:
        return render_template('add_user.html')
        

@app.route('/messages')
def messages():
    return render_template('messages.html')

app.run(debug=True)


