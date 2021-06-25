from catconnect import app
from flask import render_template, redirect, url_for, flash, request
from catconnect.models import Item, User, Cats
from catconnect.forms import RegisterForm, LoginForm, CatAdoptForm, CancelAdoptForm
from catconnect import db
from flask_login import login_user, logout_user, login_required, current_user
import urllib.request
import os
from werkzeug.utils import secure_filename
from catconnect import UPLOAD_FOLDER
from catconnect import allowed_file
from .models import Cats

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/adoptionpage', methods=['GET', 'POST'])
@login_required
def adoption_page():
    cat_adopt_form = CatAdoptForm()
    cancel_adopt_form = CancelAdoptForm()
    if request.method == "POST":
        #Cat Adoption Logic
        adopted_cats = request.form.get('adopted_cats')
        a_cats_object = Item.query.filter_by(name=adopted_cats).first()
        if a_cats_object:
            if  current_user.can_purchase(a_cats_object):
                a_cats_object.buy(current_user)
                flash(f"Congratulations! You adopted {a_cats_object.name}.", category='success')
            else:
                flash("Unfortunately, you reached the adoption limit.")
        #Cancel Adoption Logic
        returned_cats = request.form.get('returned_cats')
        r_cats_object = Item.query.filter_by(name=returned_cats).first()
        if r_cats_object:
            if current_user.can_sell(r_cats_object):
                r_cats_object.sell(current_user)
                flash(f"You returned {r_cats_object.name} back for adoption.", category='success')
            else:
                flash("Something went wrong with adoption", category='danger')

        return redirect(url_for('adoption_page'))

    if request.method == "GET":
        cats = Item.query.filter_by(owner=None)
        owned_cats = Item.query.filter_by(owner=current_user.id)
        return render_template('adoptionpage.html', cats=cats, cat_adopt_form=cat_adopt_form, owned_cats=owned_cats, cancel_adopt_form=cancel_adopt_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}.", category='success')
        return redirect(url_for('adoption_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username= form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route("/addcat", methods=['GET', 'POST'])
@login_required
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
            flash('Image successfully uploaded.')
            # return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

        cat = Cats(name=cat_name, breed=cat_breed, age=cat_age, description=cat_desc, image=filename)
        our_cats = Cats.query.order_by(Cats.date_added)
        
        db.session.add(cat)
        try:
            flash('Cat added successfully!', 'success')
            db.session.commit()
        except:
            # Add a message for unsuccessful addition of cat
            flash('Cannot add the cat. Please try again.', 'danger')
            db.session.rollback()
        db.session.commit()

        return redirect(url_for('cat_list'))

    else:
        return render_template('add_cat.html')

@app.route("/editcat/<int:id>", methods=['GET'])
@login_required
def editcat(id):

    cat = Cats.query.get(id)

    return render_template('edit_cat.html', cat=cat)

@app.route('/updatecat/<int:id>', methods=['POST'])
@login_required
def updatecat(id):

    cat_id = id
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
        flash('Image successfully uploaded.')
        # return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

    update_cat = Cats.query.get(cat_id)
    update_cat.name = cat_name
    update_cat.breed = cat_breed
    update_cat.age = cat_age
    update_cat.description = cat_desc
    update_cat.image = filename

    try:
        flash('The cat updated successfully!', 'success')
        db.session.commit()
    except:
        flash('The update was unsuccessful. Please try again.', 'danger')
        db.session.rollback()

    return redirect(url_for('cat_list'))

@app.route('/delete_cat', methods=['POST'])
@login_required
def delete_cat():

    catid = request.form['catid']
    db.session.delete(Cats.query.get(catid))
    try: 
        flash('Deletion completed!', 'success')
        db.session.commit()
    except:
        flash('Deletion was unsuccessful. Please try again', 'danger')
        db.session.rollback()

    return redirect(url_for('cat_list'))

@app.route('/catinfo/<int:cat_id>')
@login_required
def catinfo(cat_id):

    cat = Cats.query.get(cat_id)

    return render_template('cat_info.html', cat=cat)

@app.route('/adopt_cat', methods=['POST'])
def adopt_cat():

    confirmation = request.form['adopt_cat_confirm']

    if confirmation == 'confirm':
        flash('Your request is pending for approval. Please wait for more updates.', 'success')

    return redirect(url_for('cat_list'))



@app.route("/catlist")
@login_required
def cat_list():
    our_cats = Cats.query.order_by(Cats.date_added)
    return render_template('cat_list2.html', cats=our_cats)





