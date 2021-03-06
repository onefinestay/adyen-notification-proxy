import logging
import logging.config

from flask import request
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.orm.exc import NoResultFound

from adyen_notification_proxy import app
from adyen_notification_proxy.models import db, Endpoint


UUID4_LENGTH = 36
TIMEOUT = 5  # in case of bad routes. don't want to end up in the penalty box!

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s: %(message)s',
        },
    },
    'handlers': {
        'tempfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': '/tmp/adyen_proxy.log',
            'formatter': 'default',
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
    merchant_ref = request.form.get('merchantReference', '')
    ref = merchant_ref[:UUID4_LENGTH]
    url = None
    try:
        endpoint = db.session.query(Endpoint).filter(Endpoint.ref == ref).one()
        url = endpoint.url
        _logger.info("Forwarding %s to %s", ref, url)
        response = requests.post(
            url, data=request.form, headers=request.headers, timeout=TIMEOUT)

        if (response.status_code >= 400):
            _logger.info(
                "Error forwarding %s to %s: %s", ref, url, response.status_code)

    except NoResultFound:
        _logger.info("Unknown reference %s", ref)
    except ConnectionError as ex:
        _logger.info("Connection forwarding %s to %s: %s", ref, url, ex)
    except Exception as ex:
        _logger.info("Unknown error forwarding %s to %s: %s", ref, url, ex)

    # adyen gets upset if we don't reply
    return "[accepted]"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
