import pytest
from controllers.product_controller import create_product, get_products
from controllers.category_controller import create_category
import os

os.environ['TESTING'] = 'true'

def test_create_product():
    category_id = create_category("Frutas")
    assert create_product("Maçã", category_id) == True

def test_get_products():
    category_id = create_category("Frutas")
    create_product("Maçã", category_id)
    create_product("Banana", category_id)
    products = get_products()
    assert len(products) == 2
    assert products[0]['name'] == "Maçã"
    assert products[1]['name'] == "Banana"
    assert products[0]['category_name'] == "Frutas"
