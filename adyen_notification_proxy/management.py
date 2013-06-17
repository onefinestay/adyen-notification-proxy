import sys
import uuid

from flask import request

from adyen_notification_proxy import app
from adyen_notification_proxy.models import db, Endpoint

NA = "n/a"


@app.route('/')
def help():
    return """
Adyen proxy
===========

Available endpoints:

/                   (GET) display this help
/list/              (GET) list all registered endpoints
/register/          (POST callback url): register endpoint. Returns prefix
/register-for-na/   (POST callback url): register endpoint for adyen console
"""


@app.route('/list/')
def list():
    endpoints = db.session.query(Endpoint).all()
    return '\n'.join(str(e) for e in endpoints) + '\n'

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


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        db.create_all()

    app.run(host="0.0.0.0", port=5000)
