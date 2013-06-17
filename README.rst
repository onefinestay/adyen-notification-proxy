Adyen notification proxy
========================

Proxy for sharing adyen (test) notifications between multiple developers

Getting started
---------------

::

    $ pip install -r requirements.txt

    # proxy
    $ gunicorn -w 3 -b 127.0.0.1:5000 adyen_notification_proxy.proxy:app

    # management endpoint
    $ gunicorn -w 3 -b 127.0.0.1:5001 adyen_notification_proxy.management:app

    $ curl localhost:5001

    Adyen proxy
    ===========

    Available endpoints:

    /                   (GET) display this help
    /list/              (GET) list all registered endpoints
    /register/          (POST callback url): register endpoint. Returns prefix
    /register-for-na/   (POST callback url): register endpoint for adyen console

