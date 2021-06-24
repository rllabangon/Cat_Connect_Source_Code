from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warnings
db = SQLAlchemy(app)

class Cats(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key column, automatically generated IDs
    name = db.Column(db.String(80), index=True, unique=False) # book title
    #Checkpoint #1: insert your code here
    breed = db.Column(db.String(80), index=True, unique=False) #author surname
    age = db.Column(db.Integer, index=True, unique=False) #the month of book suggestion
    description = db.Column(db.String(125), index=True, unique=False) #the year of book suggestion
    image = db.Column(db.String(80), index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Get a nice printout for Book objects
    def __repr__(self):
        return "{} in: {},{}".format(self.name, self.breed, self.age, self.description)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])
def hello_world():
    our_cats = Cats.query.order_by(Cats.date_added)
    return render_template('index.html', cats=our_cats)

@app.route("/catlist")
def cat_list():
    our_cats = Cats.query.order_by(Cats.date_added)
    return render_template('cat_list.html', cats=our_cats)

@app.route("/addcat", methods=['GET', 'POST'])
def addcat():

    if request.method == 'POST':
        cat_name = request.form['cat_name']
        cat_breed = request.form['breed']
        cat_age = request.form['age']
        cat_desc = request.form['description']

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            # return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

        cat = Cats(name=cat_name, breed=cat_breed, age=cat_age, description=cat_desc, image=filename)
        our_cats = Cats.query.order_by(Cats.date_added)
        db.session.add(cat)
        db.session.commit()
        return render_template('cat_list.html', cats=our_cats)

    else:
        return render_template('add_cat.html')


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/