# -*- coding: utf-8 -*-

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from flask import Flask, render_template, make_response, abort
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from smtplib import SMTP
from random import randint
import os
from PIL import Image

from Social.data.users import User
from Social.data.news import News
from Social.data.photos import Photos
from Social.data.videos import Videos
from Social.data import db_session
from flask import request


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

user = User()
number = 0


def parse(text):  # функция для парсинга текста сообщений
    new_text = ''
    len_t = len(text)
    while len_t > 43:
        new_text += text[:43]
        new_text += '~*&^%#^*(^~&%*#('
        len_t -= 43
        text = text[43:]
    new_text += text
    return new_text


def mail(mail):  # отправка кода на почту
    global number
    number = randint(1000, 9999)
    smtpObj = SMTP('smtp.gmail.com', port=587)
    smtpObj.starttls()
    smtpObj.login('vns.social.networks@gmail.com', 'dkflxvje`,jr')
    smtpObj.sendmail("vns.social.networks@gmail.com", mail, str(number))
    smtpObj.quit()


def correct_image(name):  # проверка коррекотностм загружаемого изображения (проверка формата файла)
    if name[-7:] in ['/png\')>', '/jpg\')>'] or name[-8:] == '/jpeg\')>':
        return True
    return False


def correct_mail(mail):  # Правильно ли указана почта
    mail = str(mail)
    if '@' in mail and mail.count('@') == 1 and mail[0] != '@' and mail[mail.rfind('@'):].count('.') == 1:
        return True
    return False


class Video(FlaskForm):  # Добавление видео
    title = StringField(b'\xd0\x92\xd0\xb2\xd0\xb5\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe'.decode('utf-8'))
    file = FileField(
        b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb8\xd1\x82\xd0\xb5 \xd1\x84\xd0\xb0\xd0\xb9\xd0\xbb'.decode(
            'utf-8'))
    submit = SubmitField(b'\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c'.decode('utf-8'))


class Perepiska(FlaskForm):  #
    search = StringField(b'\xd0\x9d\xd0\xb0\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd1\x82\xd1\x8c'.decode('utf-8'),
                         validators=[DataRequired()])
    submit = SubmitField(b'\xd0\x9e\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c'.decode('utf-8'))


class StatusForm(FlaskForm):  # изменение статуса
    search = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Ok')


class Avatar(FlaskForm):  # изменение аватара
    submit = SubmitField('ADD')
    title = StringField(b'\xd0\x97\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba'.decode('utf-8'),
                        validators=[DataRequired()])
    file = FileField(
        b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb8\xd1\x82\xd0\xb5 \xd1\x84\xd0\xb0\xd0\xb9\xd0\xbb'.decode(
            'utf-8'))


class RegisterForm(FlaskForm):  # форма регистрации
    username = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    r_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Friends_form(FlaskForm):  # поиск друзей
    search = StringField(b'\xd0\x9f\xd0\xbe\xd0\xb8\xd1\x81\xd0\xba'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField(b'\xd0\x9f\xd0\xbe\xd0\xb8\xd1\x81\xd0\xba'.decode('utf-8'))


class NewsForm(FlaskForm):  # форма добавления новости
    title = StringField(b'\xd0\x97\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba'.decode('utf-8'),
                        validators=[DataRequired()])
    content = TextAreaField(
        b'\xd0\xa1\xd0\xbe\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'.decode('utf-8'))
    is_private = BooleanField(b'\xd0\x9b\xd0\xb8\xd1\x87\xd0\xbd\xd0\xbe\xd0\xb5'.decode('utf-8'))
    file = FileField(
        b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb8\xd1\x82\xd0\xb5 \xd1\x84\xd0\xb0\xd0\xb9\xd0\xbb'.decode(
            'utf-8'))
    submit = SubmitField(b'\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c'.decode('utf-8'))


class LoginForm(FlaskForm):  # форма авторизации
    email = EmailField(b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0'.decode('utf-8'), validators=[DataRequired()])
    password = PasswordField(b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c'.decode('utf-8'),
                             validators=[DataRequired()])
    remember_me = BooleanField(
        b'\xd0\x97\xd0\xb0\xd0\xbf\xd0\xbe\xd0\xbc\xd0\xbd\xd0\xb8\xd1\x82\xd1\x8c \xd0\xbc\xd0\xb5\xd0\xbd\xd1\x8f'.decode(
            'utf-8'))
    submit = SubmitField(b'\xd0\x92\xd0\xbe\xd0\xb9\xd1\x82\xd0\xb8'.decode('utf-8'))


class MS(FlaskForm):  # для начала диалога
    submit = SubmitField(
        b'\xd0\x9d\xd0\xb0\xd1\x87\xd0\xb0\xd1\x82\xd1\x8c \xd1\x80\xd0\xb0\xd0\xb7\xd0\xb3\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x80'.decode(
            'utf-8'))
    write = SubmitField(b'\xd0\x9d\xd0\xb0\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd1\x82\xd1\x8c'.decode('utf-8'))
    begin = SubmitField(
        b'\xd0\x9d\xd0\xb0\xd1\x87\xd0\xb0\xd1\x82\xd1\x8c \xd0\xb4\xd0\xb8\xd0\xb0\xd0\xbb\xd0\xbe\xd0\xb3'.decode(
            'utf-8'))


class code_verefication(FlaskForm):  # проверка кода отправленного на почту
    code = IntegerField(b'\xd0\x9a\xd0\xbe\xd0\xb4'.decode('utf-8'))
    submit = SubmitField(
        b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x82\xd0\xb2\xd0\xb5\xd1\x80\xd0\xb4\xd0\xb8\xd1\x82\xd1\x8c'.decode('utf-8'))


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def enter():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():  # авторизация
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/main/{current_user.id}")
        return render_template('login.html',
                               message=b'\xd0\x9d\xd0\xb5\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0'
                                       b'\xbd\xd1\x8b\xd0\xb9 \xd0\xbb\xd0\xbe\xd0\xb3\xd0\xb8\xd0\xbd '
                                       b'\xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbf\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c'.decode(
                                   'utf-8'),
                               form=form)
    return render_template('login.html',
                           title=b'\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f'.decode(
                               'utf-8'), form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():  # регистрация
    global user
    form = RegisterForm()
    session = db_session.create_session()
    sp = []
    for el in session.query(User).all():
        sp.append(el.email)
    if form.validate_on_submit() and form.password.data == form.r_password.data and correct_mail(form.username.data) \
            and form.username.data not in sp:
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.username.data
        user.hashed_password = form.password.data
        user.age = form.age.data
        user.modified_data = datetime.datetime.now()
        user.friends = '1'
        user.avatar = '1.png'
        mail(user.email)
        return redirect('/mail')
    return render_template('register.html',
                           title=b'\xd0\xa0\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f'.decode(
                               'utf-8'), form=form)


@app.route('/main/<int:id>', methods=['GET', 'POST'])
@login_required
def main(id):  # страница пользователя
    if id == current_user.id:
        session = db_session.create_session()
        sp_news = []
        for el in session.query(News).all():
            if str(id) == str(el.user_id):
                sp_news.append(el)
        return render_template('main.html', sp_news=list(reversed(sp_news)))
    else:
        abort(404)


@app.route('/avatar/<int:id>', methods=['GET', 'POST'])
@login_required
def avatar(id):  # меняем аватар
    form = Avatar()
    if id == current_user.id and form.submit.data and correct_image(str(form.file.data)):
        print('yes')
        session = db_session.create_session()
        image = Image.open(form.file.data)
        nomer = len(os.listdir(path="static/avatar")) + 1
        q = open(f'static/avatar/{str(nomer)}' + '.png', mode="tw", encoding='utf-8')
        image.save(f'static/avatar/{str(nomer)}' + '.png')
        user = session.query(User).filter(User.id == current_user.id).first()
        user.avatar = str(nomer) + '.png'
        session.commit()
        return redirect(f'/main/{current_user.id}')
    elif id == current_user.id:
        print(form.validate_on_submit(), correct_image(str(form.file.data)))
        return render_template('avatar.html', form=form)
    else:
        abort(404)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):  # редактирование новости
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/main/' + str(current_user.id))
        else:
            abort(404)
    return render_template('news.html',
                           title=b'\xd0\xa0\xd0\xb5\xd0\xb4\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8'.decode(
                               'utf-8'), form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):  # удаление новости
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/main/' + str(current_user.id))


@app.route('/news_fr/<int:id>', methods=['GET', 'POST'])
@login_required
def news(id):  # новостидругих пользователей
    session = db_session.create_session()
    sp_news = []
    sp_autors = []
    for el in session.query(News):
        if str(el.user_id) in str(current_user.friends).split(', ') or not el.is_private:
            sp_news.append(el)
            for ell in session.query(User):
                if str(ell.id) == str(el.user_id):
                    sp_autors.append(ell)
    return render_template('news_fr.html', sp_news=list(reversed(sp_news)), sp_autors=list(reversed(sp_autors)))


@app.route('/perepiska/<int:id>', methods=['GET', 'POST'])
@login_required
def perepiska(id):  # переписка
    form = Perepiska()
    print(1)
    if os.path.exists(f'sms/{current_user.id}-{id}.txt'):
        print(2)
        file = open(f'sms/{current_user.id}-{id}.txt', mode='rt', encoding='UTF-8')
        print(2.2)
    else:
        print(3)
        file = open(f'sms/{current_user.id}-{id}.txt', mode='tw', encoding='UTF-8')
        file1 = open(f'sms/{id}-{current_user.id}.txt', mode='tw', encoding='UTF-8')
        file = open(f'sms/{current_user.id}-{id}.txt', mode='rt', encoding='UTF-8')
    sp_d = file.readlines()
    print(2.3)
    if form.submit.data:
        print(4)
        file = open(f'sms/{current_user.id}-{id}.txt', mode='a', encoding='UTF-8')
        file1 = open(f'sms/{id}-{current_user.id}.txt', mode='a', encoding='UTF-8')
        text = form.search.data
        text = parse(text)
        session = db_session.create_session()
        for i in session.query(User).all():
            if i.id == current_user.id:
                print(i.name + ' ' + i.surname, file=file, end=b'~*&^%#^*(^~&%*#( '.decode('utf-8'))
                print(i.name + ' ' + i.surname, file=file1, end=b'~*&^%#^*(^~&%*#( '.decode('utf-8'))
                break
        print(5)
        print(text + b'~*&^%#^*(^~&%*#( '.decode('utf-8') + str(datetime.datetime.now()), file=file)
        print(text + b'~*&^%#^*(^~&%*#( '.decode('utf-8') + str(datetime.datetime.now()), file=file1)
        return redirect(f'/perepiska/{id}')
    return render_template('perepiska.html', form=form, sp_d=list(reversed(sp_d)))


@app.route('/begin/<int:id>', methods=['GET', 'POST'])
@login_required
def begin(id):  # начало диалога
    form = MS()
    session = db_session.create_session()
    sp = str(current_user.friends).split(', ')
    sp_id = list(map(int, str(current_user.friends).split(', ')))
    sp_d = []
    for i in session.query(User).all():
        if i.id in sp_id and not os.path.exists(f'sms/{current_user.id}-{i.id}.txt'):
            sp_d.append([str(i.name) + ' ' + str(i.surname), i.id, i.avatar])
    return render_template('begin.html', form=form, sp_d=sp_d)


@app.route('/sms/<int:id>', methods=['GET', 'POST'])
@login_required
def sms(id):  # выбор диалога
    form = MS()
    session = db_session.create_session()
    if len(str(current_user.friends)) > 0:
        sp_id = list(map(int, str(current_user.friends).split(', ')))
        sp_d = []
        for i in session.query(User).all():
            if i.id in sp_id and os.path.exists(f'sms/{current_user.id}-{i.id}.txt'):
                sp_d.append([str(i.name) + ' ' + str(i.surname), i.id, str(i.avatar)])
        if len(sp_d) == len(str(current_user.friends)):
            s = [len(sp_d), False] + sp_d
        else:
            s = [len(sp_d), True] + sp_d
        sp_d = s
        if form.submit.data:
            if current_user.friends:
                sp_d = []
                for i in session.query(User).all():
                    if i.id in sp_id:
                        sp_d.append((str(i.name) + ' ' + str(i.surname)))
            return redirect(f'/begin/{id}')
        elif form.write.data:
            return redirect(f'/perepiska/{id}')
        return render_template('sms.html', form=form, sp_d=sp_d)
    else:
        return redirect(f'/friends/{current_user.id}')


@app.route('/f_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def f_profile(id):  # профиль друго пользователя
    session = db_session.create_session()
    if str(current_user.id) in str(session.query(User).filter(int(id) == User.id).first().friends).split(', '):
        session = db_session.create_session()
        sp_news = []
        maaaaaan = session.query(User).filter(int(id) == User.id).first()
        for el in session.query(News).all():
            if str(id) == str(el.user_id):
                sp_news.append(el)
        return render_template('f_main.html', sp_news=sp_news, maaaaaan=maaaaaan)
    else:
        session = db_session.create_session()
        sp_news = []
        maaaaaan = session.query(User).filter(int(id) == User.id).first()
        for el in session.query(News).all():
            if str(id) == str(el.user_id) and not el.is_private:
                sp_news.append(el)
        return render_template('f_main.html', sp_news=sp_news, maaaaaan=maaaaaan)


@app.route('/friends/<int:id>', methods=['GET', 'POST'])
@login_required
def friends(id):  # поиск друзей
    form = Friends_form()
    session = db_session.create_session()
    session = db_session.create_session()
    sp_friends = []
    for el in session.query(User).all():
        if str(current_user.id) in str(el.friends).split(', '):
            sp_friends.append(el)
    if form.submit.data and form.search.data != '':
        return redirect(f'/search/{form.search.data}')
    return render_template('your_friends.html', form=form, sp_friends=sp_friends)


@app.route('/requests/<int:id>', methods=['GET', 'POST'])
@login_required
def requests(id):  # заявки в друзья
    session = db_session.create_session()
    sp_requests = []
    for el in session.query(User).all():
        if str(el.id) in str(current_user.request).split():
            sp_requests.append(el)
    return render_template('requests.html', sp_requests=sp_requests, form=Friends_form)


@app.route('/append_friend/<int:id>', methods=['GET', 'POST'])
@login_required
def append_friend(id):  # добавление друзей (кидаем заявку)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    user.request = str(user.request) + ' ' + str(current_user.id)
    session.commit()
    return redirect(f'/friends/{current_user.id}')


@app.route('/plus_friend/<int:id>', methods=['GET', 'POST'])
@login_required
def plus_friend(id):  # добавление друзей (тех, кто сам кинул заявку)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    user.friends = str(user.friends) + ', ' + str(id)
    sp = str(user.request).split()
    sp2 = []
    for el in sp:
        if el != str(id):
            sp2.append(el)
    user.request = ' '.join(sp2)
    session.commit()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    user.friends = str(user.friends) + ', ' + str(current_user.id)
    session.commit()
    return redirect(f'/requests/{current_user.id}')


@app.route('/search/<string:s>', methods=['GET', 'POST'])
@login_required
def search_friends(s): # посик по пользователям
    form = Friends_form()
    s = s.lower()
    session = db_session.create_session()
    sp_p = []
    for el in session.query(User).all():
        if (s in (el.name + el.surname).lower() or s in (el.surname + el.name).lower()) and str(el.id) not in str(
                current_user.friends).split(', ') and el.id != current_user.id and str(id) not in str(
            current_user.request).split():
            sp_p.append(el)
    if form.submit.data:
        return redirect(f'/search/{form.search.data}')
    return render_template('serch_friends.html', sp_p=sp_p, form=form)


@app.route('/friends_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def friends_delete(id):  # удаление друга
    if id != 1:
        session = db_session.create_session()
        st = str(session.query(User).filter(User.id == current_user.id).first().friends).split(', ')
        for i in range(len(st)):
            if st[i] == str(id):
                del st[i]
                break
        user = session.query(User).filter(User.id == current_user.id).first()
        user.friends = ', '.join(st)
        session.commit()
        session = db_session.create_session()
        st = str(session.query(User).filter(User.id == id).first().friends).split(', ')
        for el in session.query(User).all():
            if str(el.id) == str(id):
                user = el
                break
        for i in range(len(st)):
            if st[i] == str(current_user.id):
                del st[i]
                break
        user.friends = ', '.join(st)
        session.commit()
        return redirect(f'/friends/{current_user.id}')
    else:
        abort(404)


@app.route('/add_news/<int:id>', methods=['GET', 'POST', 'DATA'])
@login_required
def add_news(id):  # добавление новости
    form = NewsForm()
    if form.validate_on_submit() and correct_image(str(form.file.data)):
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.user_id = current_user.id
        image = Image.open(form.file.data)
        image.save(f'static/{str(session.query(Photos).all()[-1].id + 1)}' + '.png')
        photo = Photos()
        photo.name = str(session.query(Photos).all()[-1].id + 1) + '.png'
        news.Photos = session.query(Photos).all()[-1].id + 1
        session.add(photo)
        session.add(news)
        session.commit()
        return redirect('/main/' + str(current_user.id))
    elif form.validate_on_submit() and str(form.file.data) == '<FileStorage: \'\' (\'application/octet-stream\')>':
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.user_id = current_user.id
        session.add(news)
        session.commit()
        return redirect('/main/' + str(current_user.id))
    return render_template('news.html',
                           title=b'\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8'.decode(
                               'utf-8'),
                           form=form)


@app.route('/change_status/<int:id>', methods=['GET', 'POST', 'DATA'])
@login_required
def change_status(id):  # редактирование статуса
    form = StatusForm()
    if form.submit.data:
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        user.status = form.search.data
        session.commit()
        return redirect(f'/main/{current_user.id}')
    return render_template('change_status.html', form=form)


@app.route('/mail', methods=['GET', 'POST'])
def mail_verification():  # проверка почты
    global number, user
    form = code_verefication()
    if form.validate_on_submit:
        if str(number) == str(form.code.data) and str(number) != '0':
            session = db_session.create_session()
            session.add(user)
            session.commit()
            user = User()
            return redirect('/login')
        return render_template('mail.html',
                               title=b'\xd0\x9f\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe\xd1\x87\xd1\x82\xd1\x8b'.decode(
                                   'utf-8'), form=form)
    return render_template('mail.html',
                           title=b'\xd0\x9f\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe\xd1\x87\xd1\x82\xd1\x8b'.decode(
                               'utf-8'), form=form)


@app.route('/video/<int:id>', methods=['GET', 'POST'])
@login_required
def video(id):  # просмотр своиз видео и поиск новых
    form = Friends_form()
    session = db_session.create_session()
    sp = []
    for el in session.query(Videos).all():
        if str(el.id) in str(current_user.videos).split():
            sp.append(el)
    if form.submit.data:
        print(1)
        session = db_session.create_session()
        sp_v = []
        for el in session.query(Videos):
            if str(form.search.data).lower() in str(el.title).lower() and str(el.id) not in str(current_user.videos).split():
                sp_v.append(el)
        return render_template('s_video.html', sp_v=sp_v)
    return render_template('video.html', sp=sp, form=form)


@app.route('/add_video/<int:id>', methods=['GET', 'POST'])
@login_required
def add_video(id):  # добавление видео
    form = Video()
    print(form.file.data)
    if form.submit.data and '.mp4' in str(form.file.data):
        print(form.file.data)
        print(0, 1 ,2 ,23 )
        session = db_session.create_session()
        video = Videos()
        video.name = str(session.query(Videos).all()[-1].id + 1) + '.mp4'
        video.title = form.title.data
        print(1)
        session.add(video)
        session.commit()
        file = open('static/' + str(session.query(Videos).all()[-1].id) + '.mp4', 'tw')
        file = form.file.data.read()
        with open('static/' + str(session.query(Videos).all()[-1].id) + '.mp4', 'wb') as f:
            f.write(file)
            print(135)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        user.videos = str(user.videos) + ' ' + str(session.query(Videos).all()[-1].id)
        session.commit()
        return redirect('/video/' + str(current_user.id))
    return render_template('add_video.html', form=form)


@app.route('/append_video/<int:id>')
@login_required
def append_video(id):  # тоже добавление видео
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    user.videos = str(user.videos) + ' ' + str(id)
    session.commit()
    return redirect(f'/video/{id}')


@app.route('/video_delete/<int:id>')
@login_required
def video_delete(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    user.videos = str(user.videos).split()
    user.videos.remove(str(id))
    user.videos = ' '.join(user.videos)
    session.commit()
    return redirect(f'/video/{id}')


def Main():
    db_session.global_init("db/blog.sqlite")
    app.run(port=8080, host='192.168.5.9')


if __name__ == '__main__':
    Main()
