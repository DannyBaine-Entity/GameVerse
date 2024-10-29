from flask import flash, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from .app import app
from .database import db
from .models import User
import bcrypt
import os
from sqlalchemy.exc import SQLAlchemyError

# Define the folder to save profile pictures (Make sure this folder exists)
UPLOAD_FOLDER = 'static/uploads/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("landing.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'login')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')  # Get the confirm password field

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'register')
            return redirect(url_for('register'))  # Redirect back to the registration page

        user = User.query.filter((User.email == email) | (User.username == username)).first()

        if user is not None:
            flash('User already exists. Please choose a different one.', 'login')
            return redirect(url_for('login'))

        # Password conditions
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'register')
            return redirect(url_for('register'))
        elif not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'register')
            return redirect(url_for('register'))
        elif not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'register')
            return redirect(url_for('register'))
        elif not any(char.isdigit() for char in password):
            flash('Password must contain at least one numeric digit.', 'register')
            return redirect(url_for('register'))
        elif not any(char in '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~' for char in password):
            flash('Password must contain at least one special character.', 'register')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(email=email, username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('User already exists. Please choose a different one.', 'login')
        return redirect(url_for('login'))  # Redirects user to login page
    return render_template("register.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:  # Check if user is logged in
        user = User.query.get(session['user_id'])  # Get the user from the database
        if user:
            return render_template("home.html", user=user)  # Render home page with user data
        else:
            flash('User not found.', 'home')
            return redirect(url_for('login'))
    else:
        flash('You need to log in to access the home page.', 'login')
        return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:  # Check if the user is logged in
        user = User.query.get(session['user_id'])  # Get the user from the database
        if user:
            return render_template("profile.html", user=user)  # Render profile page with user data
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))  # Redirect to login if user is not found
    else:
        flash('You need to log in to access the profile page.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:  # Check if the user is logged in
        user = User.query.get(session['user_id'])  # Get the user from the database
        if user:
            if request.method == 'POST':
                # Update the username and email
                username = request.form.get('username')
                email = request.form.get('email')

                # Ensure fields are not empty
                if not username or not email:
                    flash('Username and Email are required fields.', 'danger')
                    return redirect(url_for('edit_profile'))

                user.username = username
                user.email = email

                # Handle profile picture upload
                if 'profile_pic' in request.files:
                    profile_pic = request.files['profile_pic']
                    if profile_pic and allowed_file(profile_pic.filename):
                        # Ensure the upload directory exists
                        if not os.path.exists(app.config['UPLOAD_FOLDER']):
                            os.makedirs(app.config['UPLOAD_FOLDER'])

                        filename = secure_filename(profile_pic.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        profile_pic.save(filepath)
                        user.profile_pic = filename  # Save the filename in the database

                # Save changes to the database
                try:
                    db.session.commit()
                    flash('Profile updated successfully!', 'success')
                    return redirect(url_for('profile'))
                except IntegrityError as e:
                    db.session.rollback()
                    flash(f'An error occurred while updating your profile: {str(e)}', 'danger')
                    return redirect(url_for('edit_profile'))
                except SQLAlchemyError as e:
                    db.session.rollback()
                    flash(f'An error occurred while updating your profile: {str(e)}', 'danger')
                    return redirect(url_for('edit_profile'))

            # Handle GET request (rendering the edit form with user data)
            return render_template("edit_profile.html", user=user)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))  # Redirect to login if user is not found
    else:
        flash('You need to log in to access the edit profile page.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

@app.route('/games', methods=['GET', 'POST'])
def games():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return render_template("games.html", user=user)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('You need to log in to access the games page.', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))