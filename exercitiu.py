from flask import Flask
import datetime
from flask import render_template, request, url_for, redirect,session, g
from  flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data.db'
app.config['SECRET_KEY'] = 'something more secret'

db = SQLAlchemy(app)

@app.route('/')
def homepage():
    if not session.get('username',None):
        return redirect(url_for('login'))
    return render_template('home3.html', tasks=Task.query.all())

@app.before_request
def setup():
    g.username = session.get('username', None)

@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/logout')
def logoutview():
    session['username'] = None
    return redirect(url_for('login'))

@app.route('/add-new-message',methods=('GET','POST'))
def add():
    if request.method=='POST':
        new_task = Task(mesaj=request.form['textul-mesajului'],
            timestamp=str(datetime.datetime.now()),user=session['username'])
        db.session.add(new_task)
        db.session.commit()
    return render_template('add2.html')

@app.route('/profil/<user>')
def prof(user):
    tasks=Task.query.filter_by(user=user).all()
    return render_template('profil.html',tasks = tasks)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    mesaj = db.Column(db.String)
    user = db.Column(db.String)
    timestamp = db.Column(db.String)

db.create_all()
app.run()

