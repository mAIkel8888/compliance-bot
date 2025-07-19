import pytest
from controllers.category_controller import create_category, get_categories
import os

os.environ['TESTING'] = 'true'

def test_create_category():
    assert create_category("Laticínios") == True
    # Tente criar a mesma categoria novamente
    assert create_category("Laticínios") == False

def test_get_categories():
    create_category("Frutas")
    create_category("Legumes")
    categories = get_categories()
    assert len(categories) == 2
    assert categories[0]['name'] == "Frutas"
    assert categories[1]['name'] == "Legumes"
