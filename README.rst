Adyen notification proxy
========================

Proxy for sharing adyen (test) notifications between multiple developers

Getting started
---------------

::

    $ pip install -r requirements.txt
    $ python proxy.py
    * Running on http://127.0.0.1:5000/

    $ curl localhost:5000

    Adyen proxy
    ===========

    Available endpoints:

    /                   (GET) display this help
    /list/              (GET) list all registered endpoints
    /register/          (POST callback url): register endpoint. Returns prefix
    /register-for-na/   (POST callback url): register endpoint for adyen console

