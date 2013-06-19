Adyen notification proxy
========================

Proxy for sharing adyen (test) notifications between multiple developers.

With the default setup, adyen is configured with a single endpoint to send
notifications of payments to. With multiple developers working on adyen
integration concurrently, we found they each wanted to receive such
notifications for their own test payments to their local dev servers. This
proxy allows us to "share" notifications.

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
    /register/          (POST callback url): register endpoint. Returns a uuid to
                        be prefixed to your merchant reference for routing.
                        Registering an existing url returns the existing reference


Point your adyen test account at the proxy endpoint,
`adyen-proxy.example.com:5000` and then use the management endpoint to
register local endpoints. Registering a callback will return a uuid string.
Use this as a prefix for your adyan merchant reference, and the proxy will
route incoming notifications accordingly::

    $ curl -d "http://192.168.0.4:5001" adyen-proxy.example.com:5001/register/
    9bb896c0-b714-4a4c-9fc5-97f1f476e3f9
