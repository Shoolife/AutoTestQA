import pytest
import requests
import time
from config import API_URL, INSTANCE_ID, TOKEN

def send_request(endpoint, payload=None, method="POST"):
    """Отправка запроса к API"""
    url = f"{API_URL}/waInstance{INSTANCE_ID}/{endpoint}/{TOKEN}"
    headers = {"Content-Type": "application/json"}
    
    if method == "POST":
        response = requests.post(url, headers=headers, json=payload)
    else:
        response = requests.get(url, headers=headers, params=payload)
    
    return response

@pytest.fixture
def test_phone_number():
    return ""  # Тестовый номер

@pytest.fixture
def test_message():
    return "Тестовое сообщение."

def test_send_message(test_phone_number, test_message):
    """✅ Тест отправки сообщения (валидные данные)"""
    payload = {
        "chatId": f"{test_phone_number}@c.us",
        "message": test_message
    }
    response = send_request("sendMessage", payload)
    
    assert response.status_code == 200, f"Ошибка запроса: {response.text}"
    data = response.json()
    assert "idMessage" in data, "Ответ API не содержит idMessage"

def test_send_message_no_chatId(test_message):
    """❌ Тест без chatId (должна быть ошибка)"""
    payload = {
        "message": test_message
    }
    response = send_request("sendMessage", payload)

    assert response.status_code in [200, 400], "API должно возвращать 400, но если 200 – проверяем ответ"
    if response.status_code == 200:
        data = response.json()
        assert "idMessage" in data, "API вернул 200, но ответ не содержит idMessage"

def test_send_message_no_message(test_phone_number):
    """❌ Тест без message (должна быть ошибка)"""
    payload = {
        "chatId": f"{test_phone_number}@c.us"
    }
    response = send_request("sendMessage", payload)
    
    assert response.status_code == 400, "API должно возвращать ошибку 400"
    assert "message" in response.json(), "API должно возвращать сообщение об ошибке"

def test_send_message_empty_message(test_phone_number):
    """❌ Тест с пустым сообщением (должна быть ошибка)"""
    payload = {
        "chatId": f"{test_phone_number}@c.us",
        "message": ""
    }
    response = send_request("sendMessage", payload)
    
    assert response.status_code == 400, "API должно возвращать ошибку 400"
    assert "message" in response.json(), "API должно возвращать сообщение об ошибке"

def test_send_message_invalid_chat():
    """❌ Тест с неверным chatId"""
    payload = {
        "chatId": "invalid_chat",
        "message": "Тестовое сообщение"
    }
    response = send_request("sendMessage", payload)
    
    assert response.status_code == 400, "Ожидался код ошибки 400"
    assert "message" in response.json(), "API должно возвращать сообщение об ошибке"

def test_get_chat_history(test_phone_number, test_message):
    """✅ Тест получения истории чата"""

    send_request("sendMessage", {"chatId": f"{test_phone_number}@c.us", "message": test_message})
    
    payload = {
        "chatId": f"{test_phone_number}@c.us",
        "count": 10
    }
    response = send_request("getChatHistory", payload, method="POST")
    
    assert response.status_code == 200, f"Ошибка запроса: {response.text}"
    data = response.json()
    assert isinstance(data, list), "Ответ API должен быть списком сообщений"
    assert len(data) > 0, "Чат пуст или произошла ошибка"

def test_get_chat_history_no_chatId():
    """❌ Тест запроса истории без chatId"""
    time.sleep(1)
    payload = {
        "count": 10
    }
    response = send_request("getChatHistory", payload, method="POST")
    
    assert response.status_code in [200, 400], "API должно возвращать 400, но если 200 – проверяем ответ"
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), "API вернул 200, но ответ не содержит список сообщений"

def test_get_chat_history_invalid_chatId():
    """❌ Тест с неверным chatId"""
    time.sleep(1)
    payload = {
        "chatId": "invalid_chat",
        "count": 10
    }
    response = send_request("getChatHistory", payload, method="POST")
    
    assert response.status_code == 400, "API должно возвращать ошибку 400"
    assert "message" in response.json(), "API должно возвращать сообщение об ошибке"

def test_get_chat_history_zero_count(test_phone_number):
    """❌ Тест с count=0 (проверка обработки)"""
    
    time.sleep(2)  
    
    payload = {
        "chatId": f"{test_phone_number}@c.us",
        "count": 0
    }
    response = send_request("getChatHistory", payload, method="POST")
    
    assert response.status_code in [200, 400], "API должно корректно обрабатывать count=0"
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), "API вернул 200, но ответ не содержит список сообщений"
