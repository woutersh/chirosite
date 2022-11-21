from sqlalchemy.ext.hybrid import hybrid_property
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
            return self.alias
        else:
            return '{} {}'.format(self.firstname,self.lastname)

    def set_password(self, password):
        '''genereerd een password beveiliging en stilt dit ineens in'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''check via beveiliging of het password juist is'''
        return check_password_hash(self.password_hash, password)


    def give_stripe(self):
        '''voegt een streep bij de persoon toe'''
        self.strepen =str(int(self.strepen)+1)
        db.session.commit()
        return self.strepen

    def reduce_stripe(self):
        '''checkt of de persoon wel een streep heeft en trekt er dan 1 af'''
        if int(self.strepen)>2:
            self.strepen = str(int(self.strepen) - 3)
            db.session.commit()
            return self.strepen
        else:
            self.strepen ='0'
            db.session.commit()
            return self.strepen


    def get_strepen_int(self):
        '''returned strepen als in intiger'''
        return int(self.strepen)







class Groep(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), index=True, unique=True)
    strepen = db.Column(db.String(2), index=True,default = '0')
    leider = db.relationship('Leider', backref='groep', lazy='dynamic')
    programma = db.relationship('Programma', backref='groep', lazy='dynamic')

    def __repr__(self):
        return self.name

    def programmas(self):
        '''returned een lijst van programmas van de groep'''
        return Programma.query.filter_by(groep_id= self.id).all()

    def give_stripe(self):
        '''voegt een streep bij de persoon toe'''
        self.strepen =str(int(self.strepen)+1)
        db.session.commit()
        return self.strepen

    def reduce_stripe(self):
        '''checkt of de persoon wel een streep heeft en trekt er dan 1 af'''
        if int(self.strepen)>2:
            self.strepen = str(int(self.strepen) - 3)
            db.session.commit()
            return self.strepen
        else:
            self.strepen ='0'
            db.session.commit()
            return self.strepen






class Programma(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activiteit = db.Column(db.String(500), index=True)
    datum = db.Column(db.String(45), index=True)
    time_posted = db.Column(db.DateTime, index=True, default=datetime.now)
    groep_id = db.Column(db.Integer, db.ForeignKey('groep.id'))

    def __repr__(self):
        return 'Programma van {}'.format(self.datum)


    def sortDates(self):
        '''splits de datums en zet ze op volgorde zodat ze als string gesorteerd kunnen worden'''
        split=self.datum.split('/')
        return split[2],split[1],split[0]






@login.user_loader
def load_leider(id):
    return Leider.query.get(int(id))

