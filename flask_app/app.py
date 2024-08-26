from flask import Flask, render_template, request, redirect
from tools.models import User, Message
from tools.password import check_password

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html', app=None)

@app.route('/user_manager')
def user_manager():
    users = [(user, Message.user_msgs_count(user.id())) for user in User.get_all()]
    return render_template('users_list.html', users=users, app="users")

@app.route('/remove_user', methods=['POST'])
def remove_user():
    if request.method == 'POST':
        user = User.get_by_id(int(request.form['user_id']))
        message = f"Użytkownik {user.username} (id:{user.id()})"
        if request.form['permission'] == 'yes':
            message += " - USUNIĘTY"
            if request.form['has_msgs'] == 'yes':
                [msg.remove() for msg in Message.get_all_to_user_msgs(user.id())]
            user.remove()
        else:
            message += " - USUWANIE ANULOWANE"
        return render_template('app_message.html', message=message, app="users")

@app.route('/rm_ask', methods=['POST'])
def rm_ask():
    if request.method == 'POST':
        user = User.get_by_id(int(request.form['user_id']))
        return render_template('users_rmask.html', user=user)

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        user = User.get_by_id(int(request.form['user_id']))
        user.update(request.form['username'], request.form['password'])
        msg = f"Użytkownik o id:{user.id()} został zaktualizowany."
        return render_template('app_message.html', message=msg, app="users")
    else:
        user = User.get_by_id(int(request.args.get('user_id')))
        return render_template('users_edit.html', user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        user.save()
        msg = f"Dodano użytkownika {user.username} (id:{user.id()})"
        return render_template('app_message.html', message=msg, app="users")
    else:
        return render_template('users_add.html')
        


app_data = {
    "user": None
}

@app.route('/msgs_login', methods=['POST', 'GET'])
def msgs_login():
    if request.method == 'POST':
        names = User.get_names()
        name = request.form['username']
        password = request.form['password']
        if name in names:
            user = User.get_by_name(name)
            if check_password(password, user.get_password()):
                app_data['user'] = user
                return render_template('msgs_user_panel.html', user=app_data['user'], app="msgs")
            else:
                msg = "Błędne hasło!"
                return render_template('app_message.html', message=msg, app="msg_login")
        else:
            msg = "Użytkownik nie istanieje."
            return render_template('app_message.html', message=msg, app="msg_login")
    elif request.method == 'GET':
        if app_data['user'] is not None:
            return render_template('msgs_user_panel.html', user=app_data['user'], app="msgs")
        return render_template('msgs_login.html')

@app.route('/write', methods=['POST', 'GET'])
def write():
    users = User.get_all()
    if request.method == 'POST':
        msg = "Wiadomość została wysłana."
        return render_template('app_message.html', message=msg, app="msgs")
    return render_template('msgs_write.html', user=app_data['user'], users=users, app="msgs")

@app.route('/msgs_logout')
def msgs_logout():
    app_data['user'] = None
    return redirect('msgs_login')



app.run(debug=True)