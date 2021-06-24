from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    age = db.Column(db.Integer(), nullable=False)
    breed = db.Column(db.String, nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/adoptionpage')
def adoption_page():
    cats = Item.query.all()
    return render_template('adoptionpage.html', cats=cats)




if __name__ == '__main__':
    app.run(debug=True)