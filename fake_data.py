import utils.functions as functions


def fake_data():
    conn = functions.get_database_connection()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO books(isbn, book_name, book_price, author, genre) VALUES (12345, 'The Apple MacBook Pro', 9.99, 'Jacob Lebowitz', 'Non-Fiction')")
    conn.commit()
    conn.close()


fake_data()
