import requests
from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",        #paste here the password every time since i ve changed it
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    if username == '':
        return render_template('login.html', error = 'Поле логина не может быть пустым')
    password = request.form.get('password')
    if password == '':
        return render_template('login.html', error = 'Поле пароля не может быть пустым')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if records == []:
        return render_template('login.html', error = 'Пользователя не бывает')

    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])

if __name__ == '__main__':
    app.run()