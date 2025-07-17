from database import get_db_connection

def create_shopping_list(name, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO shopping_lists (name, user_id) VALUES (?, ?)", (name, user_id))
        conn.commit()
        return cursor.lastrowid
    except:
        return None
    finally:
        conn.close()

def get_shopping_lists(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopping_lists WHERE user_id = ?", (user_id,))
    lists = cursor.fetchall()
    conn.close()
    return lists

def add_item_to_list(shopping_list_id, product_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO shopping_list_items (shopping_list_id, product_id, quantity) VALUES (?, ?, ?)", (shopping_list_id, product_id, quantity))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_list_items(shopping_list_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sli.id, p.id as product_id, p.name, sli.quantity
        FROM shopping_list_items sli
        JOIN products p ON sli.product_id = p.id
        WHERE sli.shopping_list_id = ?
    """, (shopping_list_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def get_shopping_list_by_id(list_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopping_lists WHERE id = ?", (list_id,))
    shopping_list = cursor.fetchone()
    conn.close()
    return shopping_list
