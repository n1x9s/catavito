from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import json
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CATS_DB = 'cats.json'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configurations for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'priyutkotikov@yandex.ru'
app.config['MAIL_PASSWORD'] = 'pbbsoohefvipzwql'
app.config['MAIL_DEFAULT_SENDER'] = 'priyutkotikov@yandex.ru'

mail = Mail(app)


# Helper function to load cats from JSON
def load_cats():
    if not os.path.exists(CATS_DB):
        return []
    with open(CATS_DB, 'r') as file:
        return json.load(file)


# Helper function to save cats to JSON
def save_cats(cats):
    with open(CATS_DB, 'w') as file:
        json.dump(cats, file, indent=4)


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    cats = load_cats()
    return render_template('index.html', cats=cats)


@app.route('/cat/<int:cat_id>')
def show_cat(cat_id):
    cats = load_cats()
    cat = next((c for c in cats if c['id'] == cat_id), None)
    if cat is None:
        return "Cat not found", 404
    return render_template('cat_detail.html', cat=cat)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            cats = load_cats()
            new_cat = {
                'id': len(cats) + 1,
                'name': request.form['name'],
                'description': request.form['description'],
                'image': filepath
            }
            cats.append(new_cat)
            save_cats(cats)
            flash('Котик успешно добавлен!')
            return redirect(url_for('admin'))
    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/adopt/<int:cat_id>', methods=['GET', 'POST'])
def adopt(cat_id):
    cats = load_cats()
    cat = next((c for c in cats if c['id'] == cat_id), None)
    if cat is None:
        return "Cat not found", 404
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']

        # Отправка email
        msg = Message("Заявка на приют принята",
                      recipients=[user_email])
        msg.body = "Ваша заявка на приют котика " + cat['name'] + " принята и будет рассмотрена в ближайшее время."
        mail.send(msg)

        flash('Ваша заявка принята!')
        return redirect(url_for('index'))
    return render_template('adopt_form.html', cat=cat)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
