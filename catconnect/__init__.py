# This python file is responsible for packaging the other directories.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat.db'
app.config['SECRET_KEY'] = 'ce2d1a413c1a28102085afeb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

UPLOAD_FOLDER = 'catconnect/static/uploads/'

app.secret_key = 'secret key' # secret key to defend against CORS attack
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # the path for the cat's photo file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max file size of the file upload

# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from catconnect import routes
