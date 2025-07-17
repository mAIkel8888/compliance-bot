from database import get_db_connection

def add_to_stock(user_id, product_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM stock WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        item = cursor.fetchone()
        if item:
            new_quantity = item['quantity'] + quantity
            cursor.execute("UPDATE stock SET quantity = ? WHERE id = ?", (new_quantity, item['id']))
        else:
            cursor.execute("INSERT INTO stock (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_stock(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, p.name, s.quantity
        FROM stock s
        JOIN products p ON s.product_id = p.id
        WHERE s.user_id = ?
    """, (user_id,))
    stock = cursor.fetchall()
    conn.close()
    return stock

def remove_from_stock(stock_id, quantity_to_remove):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM stock WHERE id = ?", (stock_id,))
        item = cursor.fetchone()
        if item:
            new_quantity = item['quantity'] - quantity_to_remove
            if new_quantity > 0:
                cursor.execute("UPDATE stock SET quantity = ? WHERE id = ?", (new_quantity, stock_id))
            else:
                cursor.execute("DELETE FROM stock WHERE id = ?", (stock_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
