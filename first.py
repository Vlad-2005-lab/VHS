from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from flask import Flask, render_template, make_response, abort
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from Cookies.data.jobs import Jobs
from Cookies.data.users import User
from Cookies.data.news import News
from Cookies.data import db_session
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def correct_mail(mail):
    mail = str(mail)
    if '@' in mail and mail.count('@') == 1 and mail[0] != '@' and mail[mail.rfind('@'):].count('.') == 1:
        return True
    return False


class RegisterForm(FlaskForm):
    username = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    r_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def enter():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/main/{current_user.id}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main/<int:id>', methods=['GET', 'POST'])
def main(id):
    return 'Работает'


def Main():
    db_session.global_init("db/blog.sqlite")
    session = db_session.create_session()

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    Main()
