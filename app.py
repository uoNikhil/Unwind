from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, ProfileForm
import os
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

app.config['USER_MODEL'] = User

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            session['email'] = user.email
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(email=form.email.data, fullname=form.fullname.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Get user from the session
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))

    form = ProfileForm()
    if request.method == 'GET':
        form.email.data = user.email
        form.fullname.data = user.fullname
        form.username.data = user.username

    profile_pic = get_random_profile_pic()

    if form.validate_on_submit():
        flash('Profile updated!', 'success')
        return redirect(url_for('home'))

    return render_template('profile.html', profile_pic=profile_pic, form=form)


def get_random_profile_pic():
    profile_pics_directory = os.path.join(os.getcwd(), 'static', 'images', 'profile_pic')
    profile_pics = [f for f in os.listdir(profile_pics_directory) if os.path.isfile(os.path.join(profile_pics_directory, f))]

    if profile_pics:
        return random.choice(profile_pics)
    else:
        return 'profile_pic_default.png'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/home')
def home():
    # listing all videos in the specified directory
    video_files = [f for f in os.listdir('./static/vids') if f.endswith('.mp4')]
    video_path = url_for('static', filename='vids/')
    return render_template('home.html', video_files=video_files, video_path=video_path)

