from flask import Flask, request, render_template_string, jsonify, redirect, url_for, render_template
import psycopg2
from psycopg2 import OperationalError
import os

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="mindhelp_db",
            user="elizaveta", 
            password="8246"
        )
        app.logger.debug("Database connection successful")
        return conn
    except OperationalError as e:
        app.logger.error(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Проверка подключения
    conn = get_db_connection()
    if conn is None:
        return 'Ошибка подключения к базе данных', 500

    try:
        cursor = conn.cursor()

        name = request.form.get('name')
        email = request.form.get('email')
        experience = request.form.get('experience')
        timezone = request.form.get('timezone')
        notifications = 'notifications' in request.form
        consultation_type = request.form.get('consultation-type')
        priority_topic = request.form.get('priority-topic')
        preference = request.form.get('preference')
        date = request.form.get('date')
        time = request.form.get('time')

        app.logger.debug(f"Received form data: {request.form}")

        cursor.execute('''
            INSERT INTO consultations (name, email, experience, timezone, notifications,
                consultation_type, priority_topic, preference, date, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, email, experience, timezone, notifications, consultation_type,
              priority_topic, preference, date, time))

        conn.commit()
        cursor.close()
        conn.close()

        app.logger.debug("Data successfully inserted into database.")

        return 'Спасибо за вашу заявку! Мы свяжемся с вами.'

    except Exception as e:
        app.logger.error(f"Error during data insertion: {e}")
        return 'Произошла ошибка при отправке формы.', 500
    
# Сохраняем номер телефона в базе данных или ищем его
def save_or_find_phone(phone):
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        # Проверяем, существует ли уже номер телефона в базе данных
        cursor.execute("SELECT * FROM clients WHERE phone = %s", (phone,))
        user = cursor.fetchone()

        if not user:
            # Если пользователя нет, добавляем новый номер
            cursor.execute("INSERT INTO clients (phone) VALUES (%s)", (phone,))
            conn.commit()

        conn.close()
        return phone

    except Exception as e:
        app.logger.error(f"Error while saving or finding phone: {e}")
        return None


# Словарь для хранения кодов
verification_codes = {}

@app.route('/send_code', methods=['POST'])
def send_code():
    phone = request.form.get('phone')
    if not phone:
        return jsonify({"error": "Введите номер телефона"}), 400

    # Проверяем, есть ли номер телефона в базе данных
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE phone = %s", (phone,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 400

    # Генерация фиктивного кода
    code = "0000"  # фиктивный код
    verification_codes[phone] = code  # сохраняем код в словаре

    return jsonify({"message": "Код отправлен на ваш номер телефона. Введите код для продолжения."})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    phone = request.form.get('phone')
    entered_code = request.form.get('verificationCode')

    if not phone or not entered_code:
        return jsonify({"error": "Пожалуйста, введите номер телефона и код"}), 400

    # Проверяем, существует ли номер телефона в словаре кодов
    if phone not in verification_codes:
        return jsonify({"error": "Номер телефона не найден"}), 400

    # Проверяем, совпадает ли введенный код с сохраненным
    saved_code = verification_codes[phone]
    if entered_code != saved_code:
        return jsonify({"error": "Неверный код"}), 400

    # Если код верный, перенаправляем на страницу профиля
    return redirect(url_for('profile', phone=phone))

@app.route('/profile')
def profile():
    phone = request.args.get('phone')
    if phone:
        conn = get_db_connection()
        if conn is None:
            return 'Ошибка подключения к базе данных', 500

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone = %s", (phone,))
        user = cursor.fetchone()

        if user:
            name, phone, email = user[1], user[2], user[3]
            return render_template('profile.html', name=name, phone=phone, email=email)
        else:
            return 'Пользователь не найден', 404
    else:
        return 'Ошибка: номер телефона не передан', 400


    
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone = %s OR email = %s", (phone, email))
        user = cursor.fetchone()
        if user:
            return jsonify({"error": "Пользователь с таким номером телефона или email уже существует"}), 400

        cursor.execute('''
            INSERT INTO clients (name, phone, email) 
            VALUES (%s, %s, %s)
        ''', (name, phone, email))

        conn.commit()
        cursor.close()

        # Возвращаем успешный ответ, можно также добавить редирект, если нужно
        return jsonify({"message": "Регистрация прошла успешно"}), 200

    except Exception as e:
        app.logger.error(f"Error during registration: {e}")
        return jsonify({"error": "Произошла ошибка при регистрации"}), 500

@app.route('/get_client_info', methods=['POST'])
def get_client_info():
    phone = request.json.get('phone')
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM clients WHERE phone = %s", (phone,))
        client = cursor.fetchone()
        conn.close()
        if client:
            return jsonify({"name": client[0], "email": client[1]})
        else:
            return jsonify({"message": "Client not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/certificats')
def certificats():  
    return render_template('certificats.html')

@app.route('/feedback')
def tests(): 
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)