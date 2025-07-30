from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random value in production



# Persistent user database using JSON file
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        if email in users and users[email]['password'] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid credentials.', 'error')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_users()
    if not username or not email or not password:
        flash('Please fill in all fields.', 'error')
        return render_template('login.html')
    if email in users:
        flash('Email already registered.', 'error')
        return render_template('login.html')
    users[email] = {"password": password, "username": username}
    save_users(users)
    session['user'] = email
    flash('Signup successful! You are now logged in.', 'success')
    return redirect(url_for('main'))


@app.route('/main')
def main():
    if 'user' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    users = load_users()
    return render_template('index.html', user=users.get(session['user']))


@app.route('/contacts')
def contacts():
    if 'user' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    users = load_users()
    return render_template('contacts.html', user=users.get(session['user']))


# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)