from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    mail = StringField('Почта', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Роль', coerce=int, validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')