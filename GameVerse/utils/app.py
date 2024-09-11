from flask import Flask, render_template, request, redirect, url_for
from .database import db
from .models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'

def create_app():
    """Create the Flask app instance"""

    db.init_app(app)  # Initializes the database with the app

    @app.route('/')
    def index():
        return render_template("landing.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                
                return redirect(url_for('home'))  # Redirects user to home page
            else:
                return "Wrong username or password"
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                return "Email already exists"
            new_user = User(email=email, username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) # Redirects user to login page
        return render_template("register.html")

    @app.route('/home')
    def home():
        return render_template("home.html")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run()