from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, SelectMultipleField, HiddenField, IntegerField
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
    phone_number = TextField('Phone Number*', [validators.Required("Please enter \
      your Phone Number")])
    street = TextField('Address*', [validators.Required("Please enter \
        your Address")])
    city = TextField('City*', [validators.Required("Please enter \
      your City")])
    state = TextField('State*', [validators.Required("Please enter \
      your State")])

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


class AddBooksForm(FlaskForm):
    isbn = TextField('ISBN*')
    book_name = TextField('Book Name*')
    book_price = TextField('Book Price*')
    author = TextField('Author*')
    genre = TextField('Genre*')
    submit = SubmitField('Add book!')


class AddTransactionForm(FlaskForm):
    username = TextField("Customer's Username*")
    isbn = TextField('Enter ISBN*')
    submit = SubmitField('Add transaction!')


class returnBooksForm(FlaskForm):
    username = TextField("Customer's Username*")
    isbn = TextField('Enter ISBN*')
    fee = TextField('Enter Fee if needed*')

    submit = SubmitField('Add transaction!')
