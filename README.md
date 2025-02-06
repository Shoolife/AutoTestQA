# 📖 Автоматизированное тестирование API Green API

## 🔹 Описание
Этот проект содержит автотесты для проверки работы методов API **Green API**:
- `sendMessage` – отправка сообщений в WhatsApp.
- `getChatHistory` – получение истории сообщений чата.

---

## 🚀 1. Установка окружения
### 1.1 Установите Python
Убедитесь, что у вас установлен Python **3.8+**.  
Проверить можно командой:
```sh
python --version
```
Если Python не установлен, скачайте его с [официального сайта](https://www.python.org/downloads/).

### 1.2 Создайте виртуальное окружение (опционально)
```sh
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate      # Windows
```

### 1.3 Установите зависимости
Выполните команду:
```sh
pip install -r requirements.txt
```

Файл **`requirements.txt`** должен содержать:
```
pytest
requests
```

---

## 🔹 2. Настройка API

### 2.0 Добавьте свой тестовый номер телефона
Перед запуском тестов укажите свой тестовый номер в файле `test_api.py`:
```python
@pytest.fixture
def test_phone_number():
    return "7**********"  # Тестовый номер
```

### 2.1 Получите `INSTANCE_ID` и `TOKEN`
1. Перейдите в [Green API Console](https://console.green-api.com/)
2. Создайте **Developer Instance** (если еще нет)
3. Скопируйте **INSTANCE_ID** и **TOKEN**
4. Добавьте их в файл **`config.py`**:

```python
API_URL = "https://api.green-api.com"
INSTANCE_ID = "ВАШ_ID"
TOKEN = "ВАШ_ТОКЕН"
```

---

## 🔹 3. Запуск тестов
Перейдите в папку с проектом и выполните команду:
```sh
pytest test_api.py
```

Если вам нужно **вывести только результаты тестов** без лишней информации, используйте:
```sh
pytest test_api.py -q
```

---

## 🔹 4. Описание тестов
Файл **`test_api.py`** содержит следующие тесты:

### ✅ Тесты `sendMessage`
- `test_send_message` – проверяет успешную отправку сообщения.
- `test_send_message_no_chatId` – проверяет ошибку при отсутствии `chatId`.
- `test_send_message_no_message` – проверяет ошибку при отсутствии текста сообщения.
- `test_send_message_empty_message` – проверяет ошибку при отправке пустого сообщения.
- `test_send_message_invalid_chat` – проверяет ошибку при отправке на несуществующий `chatId`.

### ✅ Тесты `getChatHistory`
- `test_get_chat_history` – получает историю чата (с ожиданием появления сообщений).
- `test_get_chat_history_no_chatId` – проверяет ошибку при отсутствии `chatId`.
- `test_get_chat_history_invalid_chatId` – проверяет ошибку при передаче несуществующего `chatId`.
- `test_get_chat_history_zero_count` – проверяет обработку `count=0`.

---


## 📌 5. Ожидаемый результат
После успешного запуска тестов вывод должен быть похож на:

```sh
test_api.py .........                                                                                              [100%]
==================================================================== 9 passed in 10.34s ====================================================================
```

Если **все тесты прошли**, значит API работает корректно! 🎉


