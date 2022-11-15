import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Leider, Programma,Groep

C_FNAME = "Hannes"
C_LNAME = "Wouters"
C_EMAIL ="woutershannes@gmail.com"
C_ADDRESS = "Waterpoel 4"
C_STATUS ='0'
C_ALIAS = "Kroemstiejen"
C_STREPEN = '0'

C_GNAME ="aspiranten"
C_GID=1
C_GSTREPEN = '0'



C_FNAME2 = "ward"
C_LNAME2 = "druyts"
C_EMAIL2 ="w@gmail.com"
C_STATUS2 ='1'
C_ALIAS2 = "wacko"
C_REKENING2 ="30"
C_AFWEZIGHEID2= "houdoe"
C_STREPEN2 = '1'

C_GNAME2 ="kerels"
C_GID2=2
C_GSTREPEN2 = '1'


class LeiderTest(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

    def test_password_hashing(self):
            l = Leider(email='h@gmail.com')
            l.set_password('cat')
            self.assertFalse(l.check_password('dog'))
            self.assertTrue(l.check_password('cat'))

    def test_getters(self):
            l = Leider()
            l.firstname = C_FNAME
            l.lastname = C_LNAME
            l.email = C_EMAIL
            l.status = C_STATUS
            l.groep_id = C_GID

            l.alias = C_ALIAS
            l.strepen = C_STREPEN

            g = Groep()
            g.name = C_GNAME
            g.strepen = C_GSTREPEN
            g.id = C_GID
            db.session.add(g)
            db.session.add(l)
            db.session.commit()


            self.assertEqual(C_ALIAS, l.alias)
            self.assertEqual(C_FNAME, l.firstname)
            self.assertEqual(C_LNAME, l.lastname)
            self.assertEqual(C_EMAIL, l.email)
            self.assertEqual(C_STREPEN, l.strepen)
            self.assertEqual(C_STATUS, l.status)
            self.assertEqual("0",l.rekening)
            self.assertEqual("aanwezig", l.afwezigheid)
            self.assertEqual(g.id, l.groep.id)
            self.assertEqual(g.strepen, l.groep.strepen)

    def test_change(self):
        l = Leider()
        l.firstname = C_FNAME
        l.lastname = C_LNAME
        l.email = C_EMAIL
        l.status = C_STATUS
        l.groep_id = C_GID
        l.alias = C_ALIAS
        l.strepen = C_STREPEN

        g = Groep()
        g.name = C_GNAME
        g.strepen = C_GSTREPEN
        g.id = C_GID
        gr =Groep()
        gr.strepen = C_GSTREPEN2
        gr.name=C_GNAME2
        gr.id = C_GID2
        db.session.add(g)
        db.session.add(gr)
        db.session.add(l)
        db.session.commit()

        self.assertEqual(C_ALIAS, l.alias)
        self.assertEqual(C_FNAME, l.firstname)
        self.assertEqual(C_LNAME, l.lastname)
        self.assertEqual(C_EMAIL, l.email)
        self.assertEqual(C_STREPEN, l.strepen)
        self.assertEqual(C_STATUS, l.status)
        self.assertEqual("0", l.rekening)
        self.assertEqual("aanwezig", l.afwezigheid)
        self.assertEqual(g.id, l.groep.id)
        self.assertEqual(g.strepen, l.groep.strepen)

        l.firstname = C_FNAME2
        l.lastname = C_LNAME2
        l.email = C_EMAIL2
        l.status = C_STATUS2
        l.groep_id = C_GID2
        l.alias = C_ALIAS2
        l.strepen = C_STREPEN2
        l.rekening = C_REKENING2
        l.afwezigheid = C_AFWEZIGHEID2

        self.assertEqual(C_ALIAS2, l.alias)
        self.assertEqual(C_FNAME2, l.firstname)
        self.assertEqual(C_LNAME2, l.lastname)
        self.assertEqual(C_EMAIL2, l.email)
        self.assertEqual(C_STREPEN2, l.strepen)
        self.assertEqual(C_STATUS2, l.status)
        self.assertEqual("30", l.rekening)
        self.assertEqual("houdoe", l.afwezigheid)
        self.assertEqual(g.id, l.groep.id)
        self.assertEqual(g.strepen, l.groep.strepen)

    def test_get_leider(self):
        l =Leider()
        l.alias =C_ALIAS
        db.session.add(l)
        db.session.commit()
        self.assertEqual(C_ALIAS,Leider.get_leider(1).alias)

    def test_give_stripe(self):
        l = Leider()
        l.strepen=0
        db.session.add(l)
        db.session.commit()
        self.assertEqual(C_STREPEN, Leider.get_leider(1).strepen)
        l.give_stripe()
        self.assertEqual(C_STREPEN2, Leider.get_leider(1).strepen)

    def test_reduce_stripe(self):
        l = Leider()
        l.strepen="0"
        l.give_stripe(1)
        db.session.add(l)
        db.session.commit()
        self.assertEqual(C_STREPEN2, Leider.get_leider(1).strepen)
        l.reduce_stripe(1)
        self.assertEqual(C_STREPEN, Leider.get_leider(1).strepen)



if __name__ == '__main__':
    unittest.main(verbosity=2)