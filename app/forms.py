import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Programma


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    afwezigheid = TextAreaField('Aanwezigheid', validators=[Length(min=0, max=100)])
    address = StringField('Adres', validators=[DataRequired()])
    alias = StringField('Bijnaam', validators=[DataRequired()])
    password = PasswordField('nieuw wachtwoord')
    password2 = PasswordField(
        'herhaal nieuw wachtwoord', validators=[EqualTo('password')])
    submit = SubmitField('Submit')




class MakeProgram(FlaskForm):
    datum = TextAreaField('Datum (dd/mm/jj)',validators=[DataRequired()])
    activiteit = TextAreaField('Programma:', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

    def validate_date(self, date):
        p = Programma.query.filter_by(datum=date.data).first()
        if p is not None:
            raise ValidationError('Deze dag heeft al een programma')

class StrepenForm(FlaskForm):
    naam = ''
    strepen = ''
    geklusd = BooleanField('3 strepen weg', default=False)
    submit = SubmitField('Submit')

class AfrekeningForm(FlaskForm):
    alias = ''
    rekening = '0'
    bedrag = StringField("Bedrag toevoegen:")
    submit = SubmitField('Submit')
    betaald = BooleanField('Betaald',default=False)