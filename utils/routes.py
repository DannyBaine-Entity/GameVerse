from flask import render_template, request, redirect, url_for, session
from .app import app
from .database import db
from .models import User
import bcrypt

@app.route('/')
def index():
    return render_template("landing.html")

from flask import flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return redirect(url_for('home'))  # Redirects user to home page
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, username=username).first()

        if user:
            flash('User already exists. Please choose a different one.', 'danger')
            return redirect(url_for('login'))

        # Password conditions
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('register'))
        elif not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return redirect(url_for('register'))
        elif not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return redirect(url_for('register'))
        elif not any(char.isdigit() for char in password):
            flash('Password must contain at least one numeric digit.', 'danger')
            return redirect(url_for('register'))
        elif not any(char.isalnum() or char in '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~' for char in password):
            flash('Password must contain at least one special character.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirects user to login page
    return render_template("register.html")


@app.route('/home')
def home():
    return render_template("home.html")