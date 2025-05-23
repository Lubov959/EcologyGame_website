
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from ..forms import LoginForm, RegistrationForm
from ..extensions import db, bcrypt
from ..models.user import Users  # Импортируем модель Users
from ..models.role import Roles

user = Blueprint('user', __name__)

# Просмотр списка пользователей
@user.route('/user', methods=['GET'])
@login_required
def show():
    users = Users.query.all()  # Получаем все записи из таблицы Users
    return render_template('user/Взрыв реактора.html', users=users)

@user.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@user.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_or_edit(id=None):
    if current_user.has_role('Администратор'):
        user_instance = None
        if id:
            user_instance = Users.query.get_or_404(id)  # Получаем пользователя по id

        if request.method == 'POST':
            mail = request.form['mail']
            user_name = request.form['user_name']
            password = request.form['password']
            role_id = request.form['role_id']

            # Хешируем пароль перед сохранением в базу данных
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            if user_instance:
                # Обновление существующего пользователя
                user_instance.mail = mail
                user_instance.user_name = user_name
                user_instance.password = hashed_password  # Обновление хешированного пароля
                user_instance.role_id = role_id
            else:
                # Добавление нового пользователя
                new_user = Users(
                    mail=mail,
                    user_name = user_name,
                    password=hashed_password,  # Сохраняем хешированный пароль
                    role_id=role_id
                )
                db.session.add(new_user)

            try:
                db.session.commit()
                flash('Пользователь успешно добавлен или обновлен!', 'success')
                return redirect(url_for('user.show'))
            except Exception as e:
                flash(f'Ошибка при сохранении пользователя: {str(e)}', 'danger')
                db.session.rollback()

        roles = Roles.query.all()
        return render_template('user/create.html', user=user_instance, roles=roles)


# Удаление пользователя
@user.route('/user/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    user_instance = Users.query.get_or_404(id)  # Получаем пользователя по id
    try:
        db.session.delete(user_instance)  # Удаляем пользователя
        db.session.commit()
        flash('Пользователь успешно удален!', 'success')
        return redirect(url_for('user.show'))
    except Exception as e:
        flash(f'Ошибка при удалении пользователя: {str(e)}', 'danger')
        db.session.rollback()


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(mail=form.mail.data).first()  # Используем поле mail
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Добро пожаловать {user.user_name}!', 'success')  # Исправлено на user_name
            return redirect(next_page) if next_page else redirect(url_for('main.show'))
        else:
            flash('Ошибка входа, пожалуйста, перепроверьте данные', 'danger')
    return render_template('user/login.html', form=form)
@user.route('/user/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # Получаем роли из базы (id, name)
    roles = get_roles()  # функция, возвращающая [(id, name), ...]
    form.role.choices = roles

    if form.validate_on_submit():
        existing_user = Users.query.filter_by(mail=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже существует.', 'danger')
            return render_template('user/register.html', form=form)
        new_user = Users(
            user_name=form.username.data,
            mail=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            role_id=form.role.data  # Сохраняем id выбранной роли
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан!', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


def get_roles ():
    try:
        roles = Roles.query.all()
        # Формируем список кортежей (id, name) для заполнения SelectField
        return [(role.id, role.name) for role in roles]
    except Exception as e:
        print(f"Ошибка получения ролей из базы: {e}")
        return []