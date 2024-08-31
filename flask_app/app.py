from flask import Flask, render_template, request, redirect
from tools.models import User, Message
from tools.password import check_password

app = Flask(__name__)

app_data = {
    'user': None,
    'all_users': User.get_all()
}

@app.route('/')
def index():
    return render_template('main.html', app=None)

@app.route('/user_manager')
def user_manager():
    users = [(user, Message.user_msgs_count(user.id())) for user in app_data['all_users']]
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
    if request.method == 'POST':
        content = request.form['content']
        recipient = int(request.form['recipient'])
        message = Message(app_data['user'].id(), recipient, content)
        message.send()
        msg = f"Wiadomość do {User.get_user_name(recipient)} została wysłana."
        return render_template('app_message.html', message=msg, app="msgs")
    return render_template('msgs_write.html', user=app_data['user'], users=app_data['all_users'], app="msgs")

@app.route('/msgs_logout')
def msgs_logout():
    app_data['user'] = None
    return redirect('msgs_login')

@app.route('/msgs_manager', methods=['POST', 'GET'])
def msgs_manager():
    return render_template('msgs_msgmanager.html', user=app_data['user'], users=app_data['all_users'], app="msgs")
    
@app.route('/receive', methods=['GET'])
def msgs_receive():
    msgs = Message.get_all_to_user_msgs(int(app_data['user'].id()))
    return render_template('msgs_list_msg.html', user=app_data['user'], users=app_data['all_users'], msgs=msgs, app="msgs", typ="receive")

@app.route('/sent', methods=['GET'])
def msgs_sent():
    msgs = Message.get_all_from_user_msgs(int(app_data['user'].id()))
    return render_template('msgs_list_msg.html', user=app_data['user'], users=app_data['all_users'], msgs=msgs, app="msgs", typ="sent")

@app.route('/show_all', methods=['GET'])
def msgs_show_all():
    msgs = Message.get_all_user_msgs(int(app_data['user'].id()))
    return render_template('msgs_list_msg.html', user=app_data['user'], users=app_data['all_users'], msgs=msgs, app="msgs", typ="all")


app.run(debug=True)

