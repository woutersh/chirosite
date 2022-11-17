from flask import render_template, flash, redirect, url_for,request
from app import app,db
from app.forms import LoginForm,MakeProgram,EditProfileForm,StrepenForm
from flask_login import current_user, login_user,logout_user, login_required
from app.models import Leider,Groep,Programma
from werkzeug.urls import url_parse
from datetime import datetime



@app.route('/')
@app.route('/index')
@login_required
def index():
    leider = {'firstname': 'Hannes'}
    groepen =Groep.query.all()
    return render_template('index.html', title='Home', leider=leider,groepen=groepen)

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

@app.route('/user/<email>/<id>')
@login_required
def leider(email,id):
    leider =Leider.query.filter_by(id=id).first_or_404()
    bezoeker = Leider.query.filter_by(email=email).first_or_404()
    return render_template('leider.html', leider=leider,bezoeker=bezoeker)

@app.route('/groep/<email>/<id>', methods=['GET', 'POST'] )
@login_required
def groep(email,id):
    leiders= Leider.query.filter_by(groep_id=id).all()
    leider = Leider.query.filter_by(email=email).first_or_404()
    groep = Groep.query.filter_by(id=id).first_or_404()
    programmas = Programma.query.filter_by(groep_id=groep.id).all()
    sorted = programmas.sort(key=lambda date: datetime.strptime(date.datum.strip(), "%d/%m/%y"))
    for p in programmas:
        if datetime.strptime(p.datum.strip(),'%d/%m/%y') < datetime.now():
            programmas.remove(p)
    form = MakeProgram()
    if form.validate_on_submit():
        program = Programma(activiteit=form.activiteit.data, datum=form.datum.data,groep=groep)
        db.session.add(program)
        db.session.commit()
        if datetime.strptime(program.datum.strip(),'%d/%m/%y') > datetime.now():
            programmas.append(program)
            flash('programma is toegevoegd')

        return render_template('groep.html',groep=groep,form =form,leider=leider,programmas=programmas\
                               ,leiders=leiders)
    return render_template('groep.html',groep=groep,form =form,leider=leider,programmas=programmas\
                                ,leiders=leiders)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.afwezigheid = form.afwezigheid.data
        current_user.alias = form.alias.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your changes have been saved.')
        return render_template('leider.html', leider=current_user)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.afwezigheid.data = current_user.afwezigheid
        form.address.data = current_user.address
        form.alias.data = current_user.alias
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/edit_programma', methods=['GET', 'POST'])
@login_required
def edit_programma():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.afwezigheid = form.afwezigheid.data
        current_user.alias = form.alias.data
        current_user.address = form.address.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return render_template('leider.html', leider=current_user)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.afwezigheid.data = current_user.afwezigheid
        form.address.data = current_user.address
        form.alias.data = current_user.alias
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
@app.route('/leiding_strepen', methods=['GET', 'POST'] )
@login_required
def leiding_strepen():
    leiders =Leider.query.all()
    form = StrepenForm()

    return render_template('strepen.html',title='strepen',list=leiders,form=form)

@app.route('/groep_strepen')
@login_required
def groep_strepen():
    form = StrepenForm()
    groepen =Groep.query.all()
    return render_template('strepen.html',title='strepen',list=groepen,form=form)