
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length,AnyOf
from app.models import Programma,Leider
from datetime import datetime
from config import Leiders,Groepen




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=80)])
    afwezigheid = TextAreaField('Aanwezigheid', validators=[Length(min=0, max=100)])
    address = StringField('Adres',validators=[DataRequired(),Length(max=120)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        leider = Leider.query.filter_by(email=email.data).first()
        if leider is not None:
            raise ValidationError('dit email adres is al in gebruik')
        email = email.data.strip()
        ongeldig = True
        for char in email:
            if char == '@':
                ongeldig = False
        if ongeldig:
            raise ValidationError('dit is geen geldig email adres')




class MakeProgram(FlaskForm):
    datum = StringField('Datum (dd/mm/jj)',validators=[DataRequired()])
    activiteit = TextAreaField('Programma:', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

    def validate_datum(self,datum):
        try:
            datetime.strptime(datum.data,'%d/%m/%y')
        except:
            raise ValidationError('Format moet DD/MM/JJ zijn')

class RegistrationForm(FlaskForm):
    firstname = StringField('Voornaam', validators=[DataRequired(),Length(min=1,max=45)])
    lastname = StringField('Achternaam', validators=[DataRequired(),Length(min=1,max=45)])
    email = StringField('Email', validators=[DataRequired(), Email(),Length(max=80)])
    address = StringField('Adres',validators=[DataRequired(),Length(max=120)])
    alias = StringField('Bijnaam', validators=[DataRequired(), Length(min=1, max=45),AnyOf(values=Leiders)])
    groep_id =StringField('Groep',validators=[DataRequired(),AnyOf(values=Groepen.keys())])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    password2 = PasswordField(
        'Herhaal Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_alias(self, alias):
        leider = Leider.query.filter_by(alias=alias.data).first()
        if leider is not None:
            raise ValidationError('dit profiel heeft al een account')

    def validate_email(self, email):
        leider = Leider.query.filter_by(email=email.data).first()
        if leider is not None:
            raise ValidationError('dit email adres is al in gebruik')
        email = email.data.strip()
        ongeldig = True
        for char in email:
            if char == '@':
                ongeldig = False
        if ongeldig:
            raise ValidationError('dit is geen geldig email adres')




class StrepenForm(FlaskForm):
    naam = ''
    strepen = ''
    geklusd = BooleanField('3 strepen weg', default=False)
    submit = SubmitField('Submit')

class AfrekeningForm(FlaskForm):
    alias = ''
    rekening = '0'
    bedrag = StringField("Bedrag toevoegen:",validators=[Length(max=7)])
    submit = SubmitField('Submit')
    betaald = BooleanField('Betaald',default=False)

    def validate_bedrag(self,bedrag):
        if bedrag.data == '' :
            bedrag.data ='0'
        try:
            float(bedrag.data)
        except:
            raise ValidationError('Je moet een getal ingeven')

class editPogramForm(FlaskForm):
    datum =''
    activiteit = TextAreaField('Programma:', validators=[Length(min=0, max=500)])
    submit = SubmitField('Save')
