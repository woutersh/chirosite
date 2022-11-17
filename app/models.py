from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Leider(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(45), index=True)
    lastname = db.Column(db.String(45), index=True)
    email = db.Column(db.String(80), index=True, unique=True)
    address = db.Column(db.String(120),index =True)
    alias = db.Column(db.String(45), index=True)
    status = db.Column(db.String(1), index=True,default ='1')
    strepen = db.Column(db.String(2), index=True,default ='0')
    rekening = db.Column(db.String(3), index=True,default = '0')
    afwezigheid = db.Column(db.String(100), index=True ,default ='aanwezig')
    password_hash = db.Column(db.String(128))
    groep_id = db.Column(db.Integer, db.ForeignKey('groep.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        if self.alias != None:
            return '{}'.format(self.alias)
        else:
            return '{} {}'.format(self.firstname,self.lastname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_leider(id):
        leider = Leider.query.get(id)
        if leider:
            return leider
        else:
            raise ValueError('geen leider gevonden met dit id')

    def give_stripe(self):
        self.strepen =str(int(self.strepen)+1)
        db.session.commit()
        return self.strepen

    def reduce_stripe(self):
        if int(self.strepen)>0:
            self.strepen = str(int(self.strepen) - 1)
            db.session.commit()
            return self.strepen
        else:return self.strepen






class Groep(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), index=True, unique=True)
    strepen = db.Column(db.String(2), index=True,default = '0')
    leider = db.relationship('Leider', backref='groep', lazy='dynamic')
    programma = db.relationship('Programma', backref='groep', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Programma(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activiteit = db.Column(db.String(500), index=True)
    datum = db.Column(db.String(45), index=True)
    time_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    groep_id = db.Column(db.Integer, db.ForeignKey('groep.id'))

    def __repr__(self):
        return 'Programma van {}'.format(self.datum)


@login.user_loader
def load_leider(id):
    return Leider.query.get(int(id))

