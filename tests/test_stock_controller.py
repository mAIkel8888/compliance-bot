import pytest
from controllers.stock_controller import *
from controllers.user_controller import create_user
from controllers.category_controller import create_category
from controllers.product_controller import create_product
import os

os.environ['TESTING'] = 'true'

@pytest.fixture
def setup_data():
    user_id = create_user("testuser", "password")
    category_id = create_category("Laticínios")
    product_id = create_product("Leite", category_id)
    return user_id, category_id, product_id

def test_add_to_stock(setup_data):
    user_id, _, product_id = setup_data
    assert add_to_stock(user_id, product_id, 5) == True
    stock = get_stock(user_id)
    assert len(stock) == 1
    assert stock[0]['quantity'] == 5

    # Adicionar mais do mesmo produto
    add_to_stock(user_id, product_id, 3)
    stock = get_stock(user_id)
    assert stock[0]['quantity'] == 8

def test_get_stock(setup_data):
    user_id, _, product_id = setup_data
    add_to_stock(user_id, product_id, 10)
    stock = get_stock(user_id)
    assert len(stock) == 1
    assert stock[0]['name'] == "Leite"

def test_remove_from_stock(setup_data):
    user_id, _, product_id = setup_data
    add_to_stock(user_id, product_id, 10)
    stock = get_stock(user_id)
    stock_id = stock[0]['id']

    # Remover uma parte
    assert remove_from_stock(stock_id, 4) == True
    stock = get_stock(user_id)
    assert stock[0]['quantity'] == 6

    # Remover tudo
    assert remove_from_stock(stock_id, 6) == True
    stock = get_stock(user_id)
    assert len(stock) == 0
