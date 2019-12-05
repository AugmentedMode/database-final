from flask import (
    Flask, render_template,
    redirect, request,
    flash, session,
    jsonify
)

from utils.forms import (
    LoginForm, SignUpForm,

    ChangeEmailForm, ChangePasswordForm,
    AddBooksForm, AddTransactionForm, returnBooksForm, EditUserForm, RefreshFeesForm

)

from flask_restful import Resource, Api, reqparse
from utils.decorators import login_required
from flask_pagedown import PageDown
from flask import Markup, request
import utils.functions as functions
import datetime
import markdown
import random

app = Flask(__name__)
api = Api(app)
pagedown = PageDown(app)
parser = reqparse.RequestParser()
app.secret_key = str(random.randint(1, 20))

@app.route('/')
@app.route('/homepage')
def home_page():
    '''
        App for hompage
    '''
    session['user_count'] = functions.get_user_count()
    try:
        if session['username']:
            return render_template('homepage.html', username=session['username'])
        return render_template('homepage.html')
    except (KeyError, ValueError):
        return render_template('homepage.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    '''
        App for creating Login page
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        user_id = functions.check_user_exists(username, password)
        if user_id:
            session['username'] = username
            session['id'] = user_id
            check_admin = functions.check_user_type(user_id)
            if check_admin:
                session['admin'] = True
            else:
                session['admin'] = False
            functions.store_last_login(session['id'])
            return redirect('/homepage')
        else:
            flash('Username/Password Incorrect!')
    return render_template('login.html', form=form)


@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    '''
        App for registering new user
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        email = request.form['email']
        phone_number = request.form['phone_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state'].upper()
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email, phone_number, street, city, state)
            session['username'] = username
            user_id = functions.check_user_exists(username, password)
            session['id'] = user_id
            return redirect('/homepage')
    return render_template('signup.html', form=form)


@app.route("/logout/")
def logout():
    '''
        App for logging out user
    '''
    session['username'] = None
    session['id'] = None
    session['admin'] = None
    return login()


@app.route("/profile/settings/change_email/", methods=['GET', 'POST'])
@login_required
def change_email():
    '''
        App for changing the email of a user
    '''
    form = ChangeEmailForm()
    if form.validate_on_submit():
        email = request.form['email']
        functions.edit_email(email, session['id'])
        return redirect('/profile/settings/')
    return render_template('change_email.html', form=form, username=session['username'])


@app.route("/profile/settings/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
    '''
        App for changing the password of a user
    '''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = request.form['password']
        functions.edit_password(password, session['id'])
        return redirect('/homepage')
    return render_template('change_password.html', form=form, username=session['username'])

@app.route("/checkout/",  methods=['GET', 'POST'])
@login_required
def checkout():
    form = AddTransactionForm()
    if form.validate_on_submit():
        isbn = request.form['isbn']
        functions.add_transaction(session['id'], isbn)
        return redirect('/homepage')
    return render_template('checkout_book.html', form=form, username=session['username'])

@app.route("/user_management/",  methods=['GET', 'POST'])
@login_required
def user_management():
    form = EditUserForm()
    if request.method == 'POST':
        id = request.form['id']
        if request.form['type'] == 'delete':
            functions.delete_user(id)
        else:
            functions.update_user_role(id)
    users_dict = functions.all_users()
    return render_template('users.html', form=form, username=session['username'], users = users_dict)

def admin():
    return 'ADMIN'

@app.route('/add_books/', methods=['GET', 'POST'])
@login_required
def add_books():
    form = AddBooksForm()
    if form.validate_on_submit():
        isbn = request.form['isbn']
        book_name = request.form['book_name']
        book_price = request.form['book_price']
        author = request.form['author']
        genre = request.form['genre']
        functions.add_to_inventory(isbn, book_name, book_price, author, genre)
        return redirect('/inventory')

    return render_template('add_books.html', form=form, username=session['username'])

@app.route('/return_books/', methods=['GET', 'POST'])
@login_required
def return_books():
    form = returnBooksForm()
    if form.validate_on_submit():
        username = request.form['username']
        isbn = request.form['isbn']
        functions.return_book(username, isbn)
        return redirect('/homepage')

    return render_template('return_books.html', form=form, username=session['username'])

@app.route("/transactions/",  methods=['GET', 'POST'])
@login_required
def transactions():
    form = RefreshFeesForm()
    if request.method == 'POST':
        functions.refresh_fees()
    trans_dict = functions.all_transactions()
    return render_template('transactions.html', form=form, username=session['username'], transactions = trans_dict)

@app.route("/inventory/",  methods=['GET', 'POST'])
@login_required
def inventory():
    inv_dict = functions.show_inventory()
    return render_template('inventory.html', username=session['username'], inventory = inv_dict)

@app.route("/my_copies/",  methods=['GET', 'POST'])
@login_required
def my_copies():
    copies_dict = functions.show_user_copies(session['id'])
    return render_template('copies.html', username=session['username'], copies = copies_dict)

if __name__ == '__main__':
    app.run(debug=True)
