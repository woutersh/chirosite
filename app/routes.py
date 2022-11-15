from flask import render_template, flash, redirect, url_for,request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user,logout_user, login_required
from app.models import Leider
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    leider = {'firstname': 'Hannes'}
    return render_template('index.html', title='Home', leider=leider)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        leider = Leider.query.filter_by(email=form.email.data).first()
        if leider is None or not leider.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(leider, remember=form.remember_me.data)
        next_page =request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<email>')
@login_required
def leider(email):
    leider = Leider.query.filter_by(email=email).first_or_404()

    return render_template('leider.html', leider=leider)