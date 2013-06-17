import sys
import uuid

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import requests
from sqlalchemy.orm.exc import NoResultFound


UUID4_LENGTH = 36
NA = "n/a"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.debug = True


@app.route('/list/')
def list():
    endpoints = db.session.query(Endpoint).all()
    return '\n'.join(str(e) for e in endpoints)

@app.route('/register/', methods=['POST'])
def register():
    url = request.data
    if url:
        ref = str(uuid.uuid4())
        endpoint = Endpoint(ref=ref, url=url)
        db.session.add(endpoint)
        db.session.commit()
        return endpoint.ref
    return "Error parsing input", 401

@app.route('/register-for-na/', methods=['POST'])
def register_for_na():
    url = request.data
    if url:
        endpoint = db.session.query(Endpoint).filter(Endpoint.ref == NA
            ).first()
        if endpoint is None:
            endpoint = Endpoint(ref="n/a")
            db.session.add(endpoint)
        endpoint.url = url
        db.session.commit()
        return endpoint.ref
    return "Error parsing input", 401


@app.route('/adyen/', methods=['POST'])
def adyen():
    merchant_ref = request.form['merchantReference']
    ref = merchant_ref[:UUID4_LENGTH]
    try:
        endpoint = db.session.query(Endpoint).filter(Endpoint.ref == ref).one()
        url = endpoint.url
        response = requests.post(url, data=request.form, headers=request.headers)
        return response.content
    except NoResultFound:
        return "Unknown endpoint", 404


class Endpoint(db.Model):
    ref = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.Text)

    def __str__(self):
        return "{}: {}".format(self.ref, self.url)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        db.create_all()

    app.run()
