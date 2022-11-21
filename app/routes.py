from flask import render_template, flash, redirect, url_for,request
from app import app,db
from app.forms import LoginForm,MakeProgram,EditProfileForm,StrepenForm,AfrekeningForm,editPogramForm,RegistrationForm
from flask_login import current_user, login_user,logout_user, login_required
from app.models import Leider,Groep,Programma
from werkzeug.urls import url_parse
from datetime import datetime
from config import Groepen




@app.route('/')
@app.route('/index')
@login_required
def index():
    leiders = Leider.query.all()
    groepen = Groep.query.all()
    prijzepot = []
    trakteren = []
    for leider in leiders:
        if int(leider.strepen)>2:
            prijzepot.append(leider)
    for groep in groepen:
        if int(groep.strepen)>2:
            trakteren.append(groep)
    return render_template('index.html', title='Home', prijzepot=prijzepot,groepen=groepen,trakteren=trakteren)


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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        leider = Leider(firstname=form.firstname.data,lastname=form.lastname.data,alias=form.alias.data,address=form.address.data, email=form.email.data)
        leider.set_password(form.password.data)
        leider.groep_id =Groepen[form.groep_id.data]
        db.session.add(leider)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Registratie', form=form)

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
    programmas = sorted(programmas,key=Programma.sortDates)
    form = MakeProgram()
    for p in programmas:
        if datetime.strptime(p.datum.strip(),'%d/%m/%y') < datetime.now():
            programmas.remove(p)
    if form.validate_on_submit():
        program = Programma(activiteit=form.activiteit.data,groep=groep,datum=form.datum.data)
        for p in programmas:
            if p.datum == program.datum:
                flash('die dag had je al iets gepland')
                return render_template('groep.html', title='groep', groep=groep, form=form, leider=leider,
                                       programmas=programmas[0:2], leiders=leiders)
        db.session.add(program)
        db.session.commit()
        if datetime.strptime(program.datum.strip(),'%d/%m/%y') > datetime.now():
            programmas.append(program)
            flash('programma is toegevoegd')
            return render_template('groep.html',title='groep',groep=groep,form =form,leider=leider,programmas=programmas[0:2]\
                               ,leiders=leiders)
    return render_template('groep.html',title='groep',groep=groep,form =form,leider=leider,programmas=programmas[0:2]\
                                ,leiders=leiders)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.afwezigheid = form.afwezigheid.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Je profiel is aangepast')
        return render_template('leider.html', leider=current_user)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.afwezigheid.data = current_user.afwezigheid
        form.address.data = current_user.address
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/leiding_strepen', methods=['GET', 'POST'] )
@login_required
def leiding_strepen():
    leiders = Leider.query.all()
    forms = []
    for leider in leiders:
        form = StrepenForm(prefix=leider.alias)
        form.naam = leider.alias
        form.strepen = leider.strepen
        forms.append(form)
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            if form.geklusd.data == True:
                l = Leider.query.filter_by(alias=form.naam).first()
                form.strepen = l.reduce_stripe()
                form.geklusd.data = False
            else:
                l = Leider.query.filter_by(alias=form.naam).first()
                form.strepen = l.give_stripe()
    return render_template('strepen.html', title='leider strepen', forms=forms)

@app.route('/groep_strepen',methods=['GET', 'POST'])
@login_required
def groep_strepen():
    groepen =Groep.query.all()
    forms=[]
    for groep in groepen:
        form = StrepenForm(prefix=groep.name)
        form.naam = groep.name
        form.strepen = groep.strepen
        forms.append(form)
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            if form.geklusd.data == True:
                g = Groep.query.filter_by(name=form.naam).first()
                form.strepen = g.reduce_stripe()
                form.geklusd.data = False
            else:
                g = Groep.query.filter_by(name=form.naam).first()

                form.strepen = g.give_stripe()
    return render_template('strepen.html',title='groep strepen',forms=forms)

@app.route('/afrekening',methods=['GET', 'POST'])
@login_required
def afrekening():
    leiders = Leider.query.order_by(Leider.groep_id).all()
    forms =[]
    for leider in leiders:
        form = AfrekeningForm(prefix=leider.alias)
        form.alias = leider.alias
        form.rekening=leider.rekening
        forms.append(form)
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            if form.betaald.data==True:
                l = Leider.query.filter_by(alias=form.alias).first()
                l.rekening ='0'
                form.rekening = l.rekening
                form.bedrag.data = ''
                form.betaald.data= False
                db.session.commit()
            else:
                l = Leider.query.filter_by(alias=form.alias).first()
                l.rekening=str(float(form.bedrag.data)+float(l.rekening))
                form.rekening= l.rekening
                form.bedrag.data=''
                db.session.commit()
    return render_template('afrekening.html', title='Afrekening', forms=forms,leiders=leiders)

@app.route('/edit_programma/<pid>',methods=['GET', 'POST'])
@login_required
def edit_programma(pid):
    programma = Programma.query.filter_by(id=pid).first_or_404()
    groep =Groep.query.filter_by(id=programma.groep_id).first_or_404()
    form = editPogramForm()
    if form.validate_on_submit():
        programma.activiteit= form.activiteit.data
        programma.time_posted = datetime.now()
        db.session.commit()
        flash('Het programma is aangepast')
        return render_template('edit_programma.html', title='Programma', programma=programma, form=form)
    elif request.method =='GET':
        form.datum= programma.datum
        form.activiteit.data=programma.activiteit
    return render_template('edit_programma.html',title='Programma',programma=programma,form=form)







