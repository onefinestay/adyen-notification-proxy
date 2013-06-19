import os

from flask.ext.sqlalchemy import SQLAlchemy

from adyen_notification_proxy import app


# default to in-memory sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite://')
db = SQLAlchemy(app)


class Endpoint(db.Model):
    ref = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.Text)

    def __str__(self):
        return "{}: {}".format(self.ref, self.url)
