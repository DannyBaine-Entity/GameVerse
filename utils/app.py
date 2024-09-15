from flask import Flask
from .database import db



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Danny_Baine/Documents/GameVerse/prisma/credentials.db'
app.secret_key = 'secret_key'

from .routes import *

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
