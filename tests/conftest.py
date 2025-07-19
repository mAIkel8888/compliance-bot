import pytest
import sqlite3
import os

@pytest.fixture(scope='session', autouse=True)
def db_connection():
    db_path = 'test_shopping_list.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    cursor.execute('''CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, FOREIGN KEY(category_id) REFERENCES categories(id))''')
    cursor.execute('''CREATE TABLE shopping_lists (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    cursor.execute('''CREATE TABLE shopping_list_items (id INTEGER PRIMARY KEY, shopping_list_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY(shopping_list_id) REFERENCES shopping_lists(id), FOREIGN KEY(product_id) REFERENCES products(id))''')
    cursor.execute('''CREATE TABLE stock (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id))''')
    conn.commit()

    yield conn

    conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture(autouse=True)
def clean_tables(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM categories")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM shopping_lists")
    cursor.execute("DELETE FROM shopping_list_items")
    cursor.execute("DELETE FROM stock")
    db_connection.commit()
