import mock

from requests.exceptions import ConnectionError
from werkzeug.datastructures import ImmutableMultiDict

from adyen_notification_proxy import proxy, app
from adyen_notification_proxy.models import Endpoint

proxy  # pyflakes, required to register views


def assert_post(mockobj, url, data, headers=mock.ANY):
    wrapped_data = ImmutableMultiDict(data)
    mockobj.post.assert_called_once_with(
        url, headers=mock.ANY, data=wrapped_data, timeout=mock.ANY)


def test_empty(db):
    with mock.patch('adyen_notification_proxy.proxy.requests') as requests:
        client = app.test_client()
        response = client.post('/adyen/', data={'merchantReference': 'foo'})
        assert not requests.post.called
        assert "[accepted]" in response.get_data()


def test_route(db):
    endpoint = Endpoint(ref='ref', url='url')
    db.session.add(endpoint)
    db.session.commit()

    with mock.patch('adyen_notification_proxy.proxy.requests') as requests:
        client = app.test_client()
        data = {'merchantReference': 'ref'}
        response = client.post('/adyen/', data=data)
        assert_post(requests, 'url', data)
        assert "[accepted]" in response.get_data()


def test_connection_error(db):
    endpoint = Endpoint(ref='ref', url='url')
    db.session.add(endpoint)
    db.session.commit()

    with mock.patch('adyen_notification_proxy.proxy.requests') as requests:
        client = app.test_client()
        data = {'merchantReference': 'ref'}
        requests.post.side_effect = ConnectionError()
        response = client.post('/adyen/', data=data)
        assert "[accepted]" in response.get_data()


def test_unknown_error(db):
    endpoint = Endpoint(ref='ref', url='url')
    db.session.add(endpoint)
    db.session.commit()

    with mock.patch('adyen_notification_proxy.proxy.requests') as requests:
        client = app.test_client()
        data = {'merchantReference': 'ref'}
        requests.post.side_effect = Exception()
        response = client.post('/adyen/', data=data)
        assert "[accepted]" in response.get_data()
