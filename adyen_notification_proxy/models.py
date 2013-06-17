import os

from flask.ext.sqlalchemy import SQLAlchemy

from adyen_notification_proxy import app


here = os.path.abspath(os.path.dirname(__file__))
make_abs = lambda fn: os.path.join(here, fn)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
    make_abs('test.db'))
db = SQLAlchemy(app)


class Endpoint(db.Model):
    ref = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.Text)

    def __str__(self):
        return "{}: {}".format(self.ref, self.url)
