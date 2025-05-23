from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from ..extensions import db
from ..models.role import Roles  # Импортируем модель Rols
from ..models.user import Users  # Импортируем модель Users

role = Blueprint('role', __name__)

# Просмотр списка ролей
@role.route('/roles', methods=['GET'])
@login_required
def show():
    roles = Roles.query.all()  # Получаем все записи из таблицы Rols
    return render_template('role/Взрыв реактора.html', roles=roles)

# Добавление или редактирование роли
@role.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@role.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_or_edit(id=None):
    role = None
    if id:
        role = Roles.query.get_or_404(id)  # Получаем роль по id

    if request.method == 'POST':
        name = request.form['name']

        if role:
            # Обновление существующей роли
            role.name = name
        else:
            # Добавление новой роли
            new_role = Roles(name=name)
            db.session.add(new_role)

        try:
            db.session.commit()
            flash('Роль успешно добавлена или обновлена!', 'success')
            return redirect(url_for('role.show'))
        except Exception as e:
            flash(f'Ошибка при сохранении роли: {str(e)}', 'danger')
            db.session.rollback()

    return render_template('role/create.html', role=role)

# Удаление роли
@role.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    role = Roles.query.get_or_404(id)  # Получаем роль по id
    try:
        db.session.delete(role)  # Удаляем роль
        db.session.commit()
        flash('Роль успешно удалена!', 'success')
        return redirect(url_for('role.show'))
    except Exception as e:
        flash(f'Ошибка при удалении роли: {str(e)}', 'danger')
        db.session.rollback()