import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Инициализация драйвера
@pytest.fixture
def driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://127.0.0.1:5000")  # Укажите URL вашей страницы
    yield driver
    driver.quit()

# Проверка наличия заголовков
def test_check_page_title(driver):
    title = driver.title
    assert title == "Психологи онлайн на MindHelp", f"Expected title 'Психологи онлайн на MindHelp', but got {title}"

# Проверка наличия формы для ввода имени
def test_name_field(driver):
    name_field = driver.find_element(By.ID, "name")
    assert name_field.is_displayed(), "Name field is not visible"
    name_field.send_keys("Иван Иванов")
    assert name_field.get_attribute("value") == "Иван Иванов", "Name input not working correctly"

# Проверка поля ввода email
def test_email_field(driver):
    email_field = driver.find_element(By.ID, "email")
    assert email_field.is_displayed(), "Email field is not visible"
    email_field.send_keys("test@example.com")
    assert email_field.get_attribute("value") == "test@example.com", "Email input not working correctly"

# Проверка выпадающего списка 'Был ли у вас опыт терапии?'
def test_experience_field(driver):
    experience_field = driver.find_element(By.ID, "experience")
    assert experience_field.is_displayed(), "Experience field is not visible"
    experience_field.click()
    experience_field.find_element(By.XPATH, "//option[@value='yes']").click()
    assert experience_field.get_attribute("value") == "yes", "Experience dropdown selection not working correctly"

# Проверка выпадающего списка 'Часовой пояс'
def test_timezone_field(driver):
    timezone_field = driver.find_element(By.ID, "timezone")
    assert timezone_field.is_displayed(), "Timezone field is not visible"
    timezone_field.click()
    timezone_field.find_element(By.XPATH, "//option[@value='other']").click()
    assert timezone_field.get_attribute("value") == "other", "Timezone dropdown selection not working correctly"

# Проверка выбора психолога и консультации
def test_therapist_selection(driver):
    consultation_type_field = driver.find_element(By.ID, "consultation-type")
    assert consultation_type_field.is_displayed(), "Consultation type field is not visible"
    consultation_type_field.click()
    consultation_type_field.find_element(By.XPATH, "//option[@value='individual']").click()
    assert consultation_type_field.get_attribute("value") == "individual", "Consultation type dropdown selection not working correctly"

# Проверка выбора предпочтений по времени
def test_time_selection(driver):
    time_field = driver.find_element(By.ID, "time")
    assert time_field.is_displayed(), "Time selection field is not visible"
    time_field.click()
    time_field.find_element(By.XPATH, "//option[@value='12:00']").click()
    assert time_field.get_attribute("value") == "12:00", "Time dropdown selection not working correctly"

# Проверка отправки формы
def test_form_submission(driver):
    # Заполнение формы
    driver.find_element(By.ID, "name").send_keys("Иван Иванов")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "experience").send_keys("yes")
    driver.find_element(By.ID, "timezone").send_keys("Moscow")
    driver.find_element(By.ID, "consultation-type").send_keys("individual")
    driver.find_element(By.ID, "priority-topic").send_keys("relationship")
    driver.find_element(By.ID, "preference").send_keys("male")
    driver.find_element(By.ID, "date").send_keys("2025-01-15")
    driver.find_element(By.ID, "time").send_keys("14:00")

    # Отправка формы
    submit_button = driver.find_element(By.CSS_SELECTOR, ".ysn-main-page-button")
    submit_button.click()

    # Проверка успешной отправки (проверьте с вашей стороны, что происходит после отправки)
    confirmation_message = driver.find_element(By.XPATH, "//div[contains(text(),'Записаться на консультацию')]")
    assert confirmation_message.is_displayed(), "Form submission failed"
