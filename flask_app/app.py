from flask import Flask, render_template, request, redirect
from tools.models import User, Message
from tools.password import check_password

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/user_manager')
def user_manager():
    users = [(user, Message.user_msgs_count(user.id())) for user in User.get_all()]
    return render_template('users.html', users=users)

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
        return render_template('rm_edit_add_msg.html', message=message)

@app.route('/rm_ask', methods=['POST'])
def rm_ask():
    if request.method == 'POST':
        user = User.get_by_id(int(request.form['user_id']))
        return render_template('rm_ask.html', user=user)

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        user = User.get_by_id(int(request.form['user_id']))
        user.update(request.form['username'], request.form['password'])
        message = f"Użytkownik o id:{user.id()} został zaktualizowany."
        return render_template('rm_edit_add_msg.html', message=message)
    else:
        user = User.get_by_id(int(request.args.get('user_id')))
        return render_template('edit_user.html', user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        user.save()
        message = f"Dodano użytkownika {user.username} (id:{user.id()})"
        return render_template('rm_edit_add_msg.html', message=message)
    else:
        return render_template('add_user.html')
        



@app.route('/messages_login', methods=['POST','GET'])
def messages():
    if request.method == 'POST':
        names = User.get_names()
        name = request.form['username']
        password = request.form['password']
        if name in names:
            user = User.get_by_name(name)
            if check_password(password, user.get_password()):
                return "Zalogowano"
            else:
                return "Błąd logowania"
        else:
            return redirect('/')
    else:
        return render_template('messages_login.html')

app.run(debug=True)


