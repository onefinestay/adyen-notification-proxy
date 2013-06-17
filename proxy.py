import pprint
import uuid

from flask import Flask, request
import requests


UUID4_LENGTH = 36

endpoints = {
    'n/a': 'http://localhost:5000/notify',
}


app = Flask(__name__)
app.debug = True


@app.route('/list/')
def list():
    return pprint.pformat(endpoints)

@app.route('/register/', methods=['POST'])
def register():
    url = request.data
    if url:
        ref = str(uuid.uuid4())
        endpoints[ref] = url
        return ref
    return "Error parsing input", 401


@app.route('/adyen/', methods=['POST'])
def adyen():
    merchant_ref = request.form['merchantReference']
    ref = merchant_ref[:UUID4_LENGTH]
    ref = 'n/a'
    try:
        url = endpoints[ref]
        response = requests.post(url, data=request.form, headers=request.headers)
        return response.content
    except KeyError:
        return "Unknown endpoint", 404


if __name__ == '__main__':
    app.run()
