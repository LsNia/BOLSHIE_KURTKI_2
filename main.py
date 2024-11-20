from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '315zxcabc123'  # Замените на ваш секретный ключ

# Конфигурация подключения к базе данных
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3839'
app.config['MYSQL_DB'] = 'fashion'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/port')
def shop():
    return render_template('port.html')

@app.route('/dashboard')
def lc():
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/cont')
def cont():
    return render_template('cont.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(usersname, pswd) VALUES(%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Вы успешно зарегестрировались', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE usersname = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session['username'] = username
            flash('Вы успешно авторизовались', 'success')
            return render_template('dashboard.html')
        else:
            flash('Пароль или логин неверен', 'danger')

    return render_template('login.html')




@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
