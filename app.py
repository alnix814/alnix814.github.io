from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from dotenv import load_dotenv
import os
import psycopg2
import datetime

app = Flask(__name__)
load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: 
            flash('Для использования сервиса, нужна авторизация', 'warning')
            return redirect(url_for('go_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute('SELECT * FROM "Users" WHERE email=%s AND password=%s', (email, password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['password'] = user[2]
        session['email'] = user[3]
        session['phone'] = user[4]
        session['user_type'] = user[5]
        session['created_at'] = user[6]

        return redirect(url_for('catalog'))
    else:
        flash('Неправильный email или пароль', 'danger')
        return render_template('index.html')

@app.route('/catalog')
@login_required
def catalog():
    username = session['username']
    return render_template('catalog.html', username=username)
    

@app.route('/go_login')
def go_login():
    return render_template('index.html')

@app.route('/go_registration')
def go_registration():
    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def registration():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        usertype = request.form.get('usertype', 'off') 


        if not all([name, email, password, phone]):
            flash('Пожалуйста, заполните все поля.', 'danger')
            return render_template('registration.html')
        

        usertype = True if usertype == 'on' else False
        created_at = datetime.datetime.now().strftime("%Y-%m-%d")

        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "Users" WHERE email = %s', (email,))
            em = cursor.fetchone()

            if em:
                flash('Данная почта уже используется', 'danger')
                return render_template('registration.html')
            else:
                cursor.execute(
                    'INSERT INTO "Users" ("username", "password", "email", "phone", "user_type", "created_at") VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, password, email, phone, usertype, created_at)
                )
                conn.commit()
                flash('Регистрация прошла успешно!', 'success')
                return render_template('index.html')
    except Exception as ex:
        flash(f'Произошла ошибка: {ex}', 'danger')
        return render_template('registration.html')

@app.route('/go_home')
def go_home():
    return render_template('home.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите, чтобы получить доступ к личному кабинету', 'warning')
        return redirect(url_for('go_login'))
    
    user_id = session['user_id']

    cursor.execute('SELECT * FROM "Users" WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()
    
    return render_template('account.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы успешно вышли из аккаунта', 'success')
    return redirect(url_for('go_home'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('go_login'))

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if session['password'] != current_password:
        flash('Неправильный текущий пароль', 'danger')
        return redirect(url_for('account'))

    if new_password != confirm_password:
        flash('Новый пароль и подтверждение не совпадают', 'danger')
        return redirect(url_for('account'))

    session['password'] = new_password
    cursor.execute('UPDATE "Users" SET password = %s WHERE user_id = %s', (new_password, session['user_id']))
    conn.commit()

    flash('Пароль успешно изменен', 'success')
    return redirect(url_for('account'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('go_login'))

    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    
    cursor.execute('UPDATE "Users" SET username = %s, email = %s, phone = %s WHERE user_id = %s',
                   (username, email, phone, session['user_id']))
    conn.commit()
    
    flash('Профиль успешно обновлен', 'success')
    return redirect(url_for('account'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    city = request.args.get('city')
    price_min = request.args.get('price_min', type=int)
    price_max = request.args.get('price_max', type=int)
    area = request.args.get('area', type=float)
    
    
    sql = """
        SELECT p.property_id, p.owner_id, p.address, p.city, p.area, p.price_per_month, p.description, p.status, p.created_at, 
            (SELECT MIN(image_url) FROM "Property_images" i WHERE i.property_id = p.property_id) AS image_url
        FROM "Properties" p
        WHERE 
            (LOWER(p.address) LIKE LOWER(%s) OR LOWER(p.description) LIKE LOWER(%s))
            AND (p.city = %s OR %s = %s)  
            AND (p.price_per_month >= %s OR %s IS NULL)  
            AND (p.price_per_month <= %s OR %s IS NULL)
            AND (p.area >= %s OR %s IS NULL)
        ORDER BY p.created_at DESC
        LIMIT 50;
    """

    params = (
    f"%{query}%", f"%{query}%", 
    city, city, city,                        
    price_min,                         
    price_min,                          
    price_max,                         
    price_max,                          
    area, area                          
    )

    try:
        cursor.execute(sql, params)
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        print("Ошибка:", e)
        return jsonify({'error': str(e)}), 500

    items = [
        {
            'property_id': row[0],
            'owner_id': row[1],
            'address': row[2],
            'city': row[3],
            'area': row[4],
            'price_per_month': row[5],
            'description': row[6],
            'status': row[7],
            'created_at': row[8],
            'image_url': row[9]
        }
        for row in results
    ]

    return jsonify({'items': items})


@app.route('/catalog_data')
def catalog_data():
    page = request.args.get('page', 1, type=int)
    per_page = 6  
    offset = (page - 1) * per_page

    sql = """
        SELECT p.property_id, p.address, p.city, p.price_per_month, 
            (SELECT MIN(image_url) FROM "Property_images" i WHERE i.property_id = p.property_id) AS image_url
        FROM "Properties" p ORDER BY p.property_id LIMIT %s OFFSET %s
    """

    cursor.execute(sql, (per_page, offset))
    print(f"SQL запрос: {cursor.query}")
    properties = cursor.fetchall()


    items = [
        {
            'property_id': prop[0],
            'address': prop[1],
            'city': prop[2],
            'price_per_month': prop[3],
            'image_url': prop[4],
        }
        for prop in properties
    ]

    return jsonify({'items': items})

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(debug=True)