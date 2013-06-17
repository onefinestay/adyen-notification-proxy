import logging
import logging.config

from flask import request
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.orm.exc import NoResultFound

from adyen_notification_proxy import app
from adyen_notification_proxy.models import db, Endpoint


UUID4_LENGTH = 36

LOG_CONFIG = {
    'version': 1,
    'handlers': {
        'tempfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': '/tmp/adyen_proxy.log',
        },
    },
    'loggers': {
        'adyen_notification_proxy': {
            'handlers': ['tempfile'],
            'level': 'INFO',
        },
    },
    '': {
        'level': 'WARNING',
    },
}

logging.config.dictConfig(LOG_CONFIG)
_logger = logging.getLogger('adyen_notification_proxy')


@app.route('/adyen/', methods=['POST'])
def adyen():
    merchant_ref = request.form['merchantReference']
    ref = merchant_ref[:UUID4_LENGTH]
    try:
        endpoint = db.session.query(Endpoint).filter(Endpoint.ref == ref).one()
        url = endpoint.url
        _logger.info("Forwarding %s to %s", ref, url)
        response = requests.post(
            url, data=request.form, headers=request.headers)
        return response.content
    except NoResultFound:
        _logger.info("Unknown reference %s", ref)
        return "Unknown endpoint", 404
    except ConnectionError as ex:
        _logger.info("Error forwarding %s to %s: %s", ref, url, ex)
        return "Connection error", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
