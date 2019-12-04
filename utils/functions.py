import os
import hashlib


def get_database_connection():
    '''
        Creates a connection between selected database
    '''
    import sqlite3
    sqlite_file = 'database.db'
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    if os.stat(sqlite_file).st_size == 0:
        create_sqlite_tables(conn)
    return conn


def create_sqlite_tables(conn):
    '''
        Creates a sqlite table as specified in schema_sqlite.sql file
    '''
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()


def get_user_count():
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def check_user_exists(username, password):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def store_last_login(user_id):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE user_id=?", (user_id, ))
        conn.commit()
        cursor.close()
    except:
        cursor.close()


def check_username(username):
    '''
        Checks whether a username is already taken or not
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
        if cursor.fetchone():
            return True
    except:
        return False


def check_user_type(user_id):
    '''
        Checks whether a username is already taken or not
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM staff WHERE user_id=?', (int(user_id), ))

        if cursor.fetchone() is not None:
            return True

        else:
            return False

    except Exception as e:
        print('whyyyyy')
        print(e)
        return False


def signup_user(username, password, email, phone_number, street, city, state):
    '''
        Function for storing the details of a user into the database
        while registering
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email, phone_number, street, city, state) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, email, phone_number, street, city, state))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def generate_password_hash(password):
    '''
        Function for generating a password hash
    '''
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()


def edit_password(password, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    password = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE user_id=?", (password, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def add_to_inventory(isbn, book_name, book_price, author, genre):
    print('HELLOOOOO')
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books(isbn, book_name, book_price, author, genre) VALUES (?, ?, ?, ?, ?)", (isbn, book_name, book_price, author, genre))
        cursor.execute("INSERT INTO copies(availability, isbn) VALUES (?, ?)", (1, isbn))

        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()
