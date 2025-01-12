import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000")  
    yield driver
    driver.quit()

def test_logo_visibility(driver):
    # Проверка видимости логотипа
    logo = driver.find_element(By.CSS_SELECTOR, ".header__logo")
    assert logo.is_displayed(), "Логотип не отображается на главной странице"

def test_navigation_menu(driver):
    # Проверка наличия основных пунктов меню
    menu_items = driver.find_elements(By.CSS_SELECTOR, ".navbar-nav .nav-item")
    expected_items = ["Обратная связь", "Сертификаты", "Вход"]
    
    menu_text = [item.text for item in menu_items]
    for item in expected_items:
        assert item in menu_text, f"Меню не содержит пункт: {item}"

def test_banner_toggle_for_self(driver):
    # Проверка функциональности переключателя для выбора "Для себя"
    toggle = driver.find_element(By.ID, "banner__toggle_head")
    toggle.click()  # Переключение на "Для двоих"
    
    price_for_self = driver.find_element(By.CSS_SELECTOR, ".price__single")
    assert price_for_self.is_displayed(), "Цена для 'Для себя' не отображается"

def test_banner_toggle_for_couple(driver):
    # Проверка функциональности переключателя для выбора "Для двоих"
    toggle = driver.find_element(By.ID, "banner__toggle_head")
    toggle.click()  # Переключение обратно на "Для себя"
    
    price_for_couple = driver.find_element(By.CSS_SELECTOR, ".price__couple")
    assert price_for_couple.is_displayed(), "Цена для 'Для двоих' не отображается"

def test_help_section(driver):
    # Проверка блока с помощью психолога
    helps_section = driver.find_element(By.CSS_SELECTOR, ".helps__content")
    assert helps_section.is_displayed(), "Блок помощи психолога не отображается на странице"
    
    help_items = driver.find_elements(By.CSS_SELECTOR, ".helps__item")
    assert len(help_items) > 0, "Список с услугами психолога пустой"

def test_therapist_section(driver):
    # Проверка секции "Как мы выбираем лучших специалистов"
    therapist_section = driver.find_element(By.CSS_SELECTOR, ".therapist__content")
    assert therapist_section.is_displayed(), "Секция 'Как мы выбираем лучших специалистов' не отображается"
    
    therapist_items = driver.find_elements(By.CSS_SELECTOR, ".therapist__item")
    assert len(therapist_items) > 0, "Информация о критериях выбора специалистов отсутствует"

def test_redirect_to_auth_page(driver):
    # Проверка перехода на страницу авторизации
    auth_button = driver.find_element(By.CSS_SELECTOR, ".header__link[href='/auth']")
    auth_button.click()
    time.sleep(2)  # Ожидание загрузки страницы
    assert "auth" in driver.current_url, "Не удалось перейти на страницу авторизации"
