from database import get_db_connection

def create_product(name, category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, category_id) VALUES (?, ?)", (name, category_id))
        conn.commit()
        return cursor.lastrowid
    except:
        return None
    finally:
        conn.close()

def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
    """)
    products = cursor.fetchall()
    conn.close()
    return products
