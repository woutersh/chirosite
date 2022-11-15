from app import app, db
from app.models import Leider, Groep , Programma


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Leider': Leider, 'Groep': Groep,'Programma': Programma}
