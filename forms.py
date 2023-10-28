from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import current_app
from flask import session



class RegistrationForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    fullname = StringField('Fullname',
                            validators=[DataRequired(), Length(min=2, max=50)])

    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

"""
class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        User = current_app.config['USER_MODEL']
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != current_user.username:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        User = current_app.config['USER_MODEL']
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != current_user.email:
            raise ValidationError('That email is taken. Please choose a different one.')
"""

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        User = current_app.config['USER_MODEL']
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != session['username']:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        User = current_app.config['USER_MODEL']
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != session['email']:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class ProfileForm(FlaskForm):
    email = StringField('Email')
    fullname = StringField('Full Name')
    username = StringField('Username')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update')