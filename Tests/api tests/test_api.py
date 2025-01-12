import pytest
import requests

BASE_URL = "http://localhost:5000"  

# Тест 1: Проверка успешной регистрации
def test_register_success():
    data = {
        "name": "Иван Иванов",
        "phone": "1234567890",
        "email": "ivan@example.com"
    }
    response = requests.post(f"{BASE_URL}/register", data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Регистрация прошла успешно"

# Тест 2: Проверка регистрации с уже существующим номером телефона
def test_register_existing_phone():
    data = {
        "name": "Иван Иванов",
        "phone": "1234567890", 
        "email": "newivan@example.com"
    }
    response = requests.post(f"{BASE_URL}/register", data=data)
    assert response.status_code == 400
    assert "Пользователь с таким номером телефона или email уже существует" in response.json()["error"]

# Тест 3: Отправка кода на номер телефона
def test_send_code_success():
    data = {"phone": "1234567890"}  
    response = requests.post(f"{BASE_URL}/send_code", data=data)
    assert response.status_code == 200
    assert "Код отправлен на ваш номер телефона" in response.json()["message"]

# Тест 4: Верификация кода
def test_verify_code_success():
    data = {
        "phone": "1234567890",  
        "verificationCode": "0000"  
    }
    response = requests.post(f"{BASE_URL}/verify_code", data=data)
    assert response.status_code == 302  # Ожидаем редирект на профиль
    assert response.headers["Location"] == "/profile?phone=1234567890"

# Тест 5: Получение информации о клиенте
def test_get_client_info_success():
    data = {"phone": "1234567890"}  
    response = requests.post(f"{BASE_URL}/get_client_info", json=data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert "email" in response.json()

# Тест 6: Получение информации о несуществующем клиенте
def test_get_client_info_not_found():
    data = {"phone": "0000000000"}  
    response = requests.post(f"{BASE_URL}/get_client_info", json=data)
    assert response.status_code == 404
    assert "Client not found" in response.json()["message"]

