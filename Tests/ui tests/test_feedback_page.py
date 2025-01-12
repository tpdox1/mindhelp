from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

# Фикстура для инициализации веб-драйвера
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Используйте драйвер, соответствующий вашему браузеру
    driver.get("http://localhost:5000")  # Замените на URL вашей страницы
    yield driver
    driver.quit()

# Тест 1: Проверка наличия логотипа в хедере
def test_logo_display(driver):
    logo = driver.find_element(By.CLASS_NAME, "header__logo")
    assert logo.is_displayed(), "Логотип не отображается"

# Тест 2: Проверка наличия ссылки на "Обратную связь" в навигации
def test_feedback_link(driver):
    feedback_link = driver.find_element(By.LINK_TEXT, "Обратная связь")
    assert feedback_link.is_displayed(), "Ссылка на обратную связь не отображается"
    assert feedback_link.get_attribute("href") == "http://localhost:5000/feedback", "Неверный URL для обратной связи"

# Тест 3: Проверка формы обратной связи
def test_feedback_form(driver):
    form = driver.find_element(By.TAG_NAME, "form")
    assert form.is_displayed(), "Форма обратной связи не отображается"

    name_input = driver.find_element(By.ID, "name")
    email_input = driver.find_element(By.ID, "email")
    message_input = driver.find_element(By.ID, "message")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

    assert name_input.is_displayed(), "Поле для имени не отображается"
    assert email_input.is_displayed(), "Поле для email не отображается"
    assert message_input.is_displayed(), "Поле для сообщения не отображается"
    assert submit_button.is_displayed(), "Кнопка отправки не отображается"

# Тест 4: Проверка успешной отправки формы
def test_form_submission(driver):
    name_input = driver.find_element(By.ID, "name")
    email_input = driver.find_element(By.ID, "email")
    message_input = driver.find_element(By.ID, "message")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

    name_input.send_keys("Иван Иванов")
    email_input.send_keys("ivan@example.com")
    message_input.send_keys("Это тестовое сообщение.")

    submit_button.click()

    # Здесь проверяем редирект или сообщение об успешной отправке
    # Замените на соответствующий URL или текст
    assert driver.current_url == "http://localhost:5000/feedback/thank_you", "Ошибка при отправке формы"

# Тест 5: Проверка кнопки "Вход" в хедере
def test_login_button(driver):
    login_button = driver.find_element(By.LINK_TEXT, "Вход")
    assert login_button.is_displayed(), "Кнопка 'Вход' не отображается"
    assert login_button.get_attribute("href") == "http://localhost:5000/auth", "Неверный URL для страницы входа"
