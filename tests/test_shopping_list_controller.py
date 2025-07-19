import pytest
from controllers.shopping_list_controller import *
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

def test_create_shopping_list(setup_data):
    user_id, _, _ = setup_data
    list_id = create_shopping_list("Lista de Teste", user_id)
    assert list_id is not None

def test_get_shopping_lists(setup_data):
    user_id, _, _ = setup_data
    create_shopping_list("Lista 1", user_id)
    create_shopping_list("Lista 2", user_id)
    lists = get_shopping_lists(user_id)
    assert len(lists) == 2

def test_add_item_to_list(setup_data):
    user_id, _, product_id = setup_data
    list_id = create_shopping_list("Minha Lista", user_id)
    assert add_item_to_list(list_id, product_id, 2) == True

def test_get_list_items(setup_data):
    user_id, _, product_id = setup_data
    list_id = create_shopping_list("Minha Lista", user_id)
    add_item_to_list(list_id, product_id, 3)
    items = get_list_items(list_id)
    assert len(items) == 1
    assert items[0]['name'] == "Leite"
    assert items[0]['quantity'] == 3

def test_get_shopping_list_by_id(setup_data):
    user_id, _, _ = setup_data
    list_id = create_shopping_list("Lista de Teste", user_id)
    retrieved_list = get_shopping_list_by_id(list_id)
    assert retrieved_list is not None
    assert retrieved_list['id'] == list_id
    assert retrieved_list['name'] == "Lista de Teste"
