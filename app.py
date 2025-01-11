from flask import Flask, request, render_template_string
import psycopg2
from psycopg2 import OperationalError

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
    return render_template_string(open('index.html').read())

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

if __name__ == '__main__':
    app.run(debug=True)
