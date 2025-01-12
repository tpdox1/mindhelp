import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("URL_вашего_сайта")  # Замените на URL вашего сайта
    yield driver
    driver.quit()

def test_send_code(driver):
    # Находим поле для ввода телефона и кнопку отправки
    phone_input = driver.find_element(By.ID, "loginPhone")
    send_button = driver.find_element(By.ID, "sendCodeButton")
    
    # Вводим номер телефона
    phone_input.send_keys("1234567890")  # Замените на тестовый номер
    send_button.click()
    
    # Ждем некоторое время, чтобы увидеть результат
    time.sleep(2)
    
    # Проверяем, что форма для ввода кода появляется
    verification_form = driver.find_element(By.ID, "verificationForm")
    assert verification_form.is_displayed(), "Форма для ввода кода не появилась"

def test_verify_code(driver):
    # Находим поля для ввода телефона и кода
    phone_input = driver.find_element(By.ID, "loginPhone")
    send_button = driver.find_element(By.ID, "sendCodeButton")
    verification_code_input = driver.find_element(By.ID, "verificationCode")
    login_button = driver.find_element(By.XPATH, "//button[text()='Войти']")
    
    # Вводим номер телефона и отправляем код
    phone_input.send_keys("1234567890")
    send_button.click()
    time.sleep(2)
    
    # Проверяем, что форма для ввода кода появилась
    verification_form = driver.find_element(By.ID, "verificationForm")
    assert verification_form.is_displayed(), "Форма для ввода кода не появилась"
    
    # Вводим код и нажимаем на кнопку входа
    verification_code_input.send_keys("0000")  # Замените на тестовый код
    login_button.click()
    
    # Ждем и проверяем успешный редирект или сообщение
    time.sleep(2)
    assert driver.current_url == "URL_профиля_пользователя", "Пользователь не был перенаправлен на профиль"

def test_registration(driver):
    # Находим форму для регистрации
    register_name_input = driver.find_element(By.ID, "registerName")
    register_phone_input = driver.find_element(By.ID, "registerPhone")
    register_email_input = driver.find_element(By.ID, "registerEmail")
    register_button = driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']")
    
    # Заполняем форму регистрации
    register_name_input.send_keys("Test User")
    register_phone_input.send_keys("1234567890")
    register_email_input.send_keys("testuser@example.com")
    
    # Отправляем форму
    register_button.click()
    
    # Ждем и проверяем успешный редирект на профиль
    time.sleep(2)
    assert driver.current_url == "URL_профиля_пользователя", "Пользователь не был перенаправлен на профиль"

