import pytest
from controllers.user_controller import create_user, authenticate_user
import os

os.environ['TESTING'] = 'true'

def test_create_user():
    assert create_user("testuser", "password123") == True
    # Tente criar o mesmo usuário novamente
    assert create_user("testuser", "password123") == False

def test_authenticate_user():
    create_user("testuser_auth", "password123")
    user = authenticate_user("testuser_auth", "password123")
    assert user is not None
    assert user['username'] == "testuser_auth"

    # Senha incorreta
    user = authenticate_user("testuser_auth", "wrongpassword")
    assert user is None

    # Usuário inexistente
    user = authenticate_user("nonexistentuser", "password123")
    assert user is None
