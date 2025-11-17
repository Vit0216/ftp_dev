from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.models.user import User
from .forms import LoginForm, RegistrationForm


auth_bp = Blueprint("auth", __name__)



@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('upload.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
       
        if User.query.filter_by(email=form.email.data).first():
            flash('Este e-mail já está registrado.', 'danger')
            return redirect(url_for('auth.registrar'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Este nome de utilizador já está em uso.', 'danger')
            return redirect(url_for('auth.registrar'))

        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registro concluído com sucesso! Pode fazer login agora.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Login efetuado com sucesso!', 'success')

        return redirect(url_for('upload.index'))
    
    return render_template("login.html", form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('auth.login'))


