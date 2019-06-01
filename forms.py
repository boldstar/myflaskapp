from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Required, Length

# @desc Register form class for the register route
class RegisterForm(FlaskForm):
    name = StringField('Name', [Length(min=1, max=50)])
    username = StringField('Username', [Length(min=4, max=25)])
    email = StringField('Email', [Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords Do Not Match')
    ])
    confirm = PasswordField('Confirm Password')

# @desc Register form class for the register route
class LoginForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])