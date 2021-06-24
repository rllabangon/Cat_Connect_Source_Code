from catconnect import db, login_manager
from catconnect import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    limit = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.limit >= item_obj.age

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    age = db.Column(db.Integer(), nullable=False)
    breed = db.Column(db.String, nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.limit -= self.age
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.limit += self.age
        db.session.commit()


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

