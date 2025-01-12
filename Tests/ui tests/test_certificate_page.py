import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Замените на нужный драйвер, если используется другой
    driver.get("http://localhost:5000")  # Замените на URL вашей локальной страницы
    yield driver
    driver.quit()

def test_main_page_title(driver):
    assert driver.title == "Подача сертификата - MindHelp"

def test_banner_section(driver):
    banner_title = driver.find_element(By.CLASS_NAME, "banner__title-h1")
    assert banner_title.text == "Получить сертификат"

def test_banner_button(driver):
    button = driver.find_element(By.CLASS_NAME, "banner__btn")
    assert button.text == "Получить сертификат"
    button.click()  # Проверяем, что кнопка работает
    time.sleep(2)  # Ждем 2 секунды для перехода на новую страницу
    assert driver.current_url == "http://localhost:5000/auth"  # Проверка редиректа
