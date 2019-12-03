from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, SelectMultipleField, HiddenField
from flask_pagedown.fields import PageDownField
from wtforms import validators


class LoginForm(FlaskForm):
    username = TextField('Username*', [validators.Required("Please enter \
      your name.")])
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password.")])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = TextField('Username*', [validators.Required("Please enter \
      your username")])
    email = TextField('Email*', [validators.Required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.Required("Confirm \
      your password")])
    submit = SubmitField('Signup')


class ChangeEmailForm(FlaskForm):
    email = TextField('Email*', [validators.Required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    submit = SubmitField('Update Email')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.Required("Confirm \
      your password")])
    submit = SubmitField('Update Password')
