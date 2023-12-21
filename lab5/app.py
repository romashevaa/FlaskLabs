import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'sheva'
csrf = CSRFProtect(app)


def load_users():
    file_path = os.path.join(app.root_path, 'static', 'clients.json')
    with open(file_path, 'r') as f:
        return json.load(f)


users = load_users()
user_cookies = {}

csrf = CSRFProtect(app)
csrf.init_app(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/info')
def info():
    username = session.get('username', None)
    user_info = users.get(username, None)

    if user_info:
        return render_template('info.html', user_info=user_info)

    flash('User not found. Please log in.', 'error')
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('message', None)
    user_cookies.clear()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    username = session.get('username', None)

    if username:
        key = request.form['cookie_key']
        value = request.form['cookie_value']
        user_cookies[key] = {"value": value,
                             "creation_time": str(datetime.datetime.now())}

    return redirect(url_for('info'))


@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    username = session.get('username', None)

    if username:
        key = request.form['delete_cookie_key']

        if key in user_cookies:
            user_cookies.pop(key)

    return redirect(url_for('info'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = session.get('username', None)

    if username:
        if request.method == 'POST':
            new_password = request.form.get('new_password')

            if new_password:
                change_user_password(username, new_password)
                flash('Password changed successfully!', 'success')

    return redirect(url_for('info'))


def change_user_password(username, new_password):
    with open('static/clients.json', 'r+') as f:
        users = json.load(f)

        if username in users:
            users[username]['password'] = new_password
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()


if __name__ == '__main__':
    app.run(debug=True)
