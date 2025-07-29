from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple user database (for demo only - use a real DB in production)
users = {
    "test@example.com": {"password": "123", "username": "testuser"}
}

@app.route('/')
def home():
    # Redirect to login page by default
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('')
        password = request.form.get('password')
        
        # Check credentials (demo only - insecure!)
        if email in users and users[email]['password'] == password:
            return redirect(url_for('main'))
        
        # If login fails, stay on login page
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Add to "database" (demo only)
    users[email] = {"password": password, "username": username}
    
    # Redirect to main page after signup
    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)