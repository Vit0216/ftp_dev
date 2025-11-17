from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6)
    ])

    confirm_password = PasswordField('Confirmar senha', validators=[
        DataRequired(),
        EqualTo('password', message="As senhas devem ser iguais.")
    ])

    submit = SubmitField('Criar conta')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Nome de Utilizador', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Senha',
        validators=[
            DataRequired(),
            EqualTo('password', message='As senhas devem ser iguais.')
        ]
    )
    submit = SubmitField('Registar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de utilizador já está a ser utilizado.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este email já está registado.')
