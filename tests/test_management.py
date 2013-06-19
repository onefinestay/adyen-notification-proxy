from adyen_notification_proxy import management, app
from adyen_notification_proxy.models import Endpoint

management  # pyflakes, required to register views


def test_index():
    client = app.test_client()
    response = client.get('/')
    assert "display this help" in response.get_data()


def test_register(db):
    client = app.test_client()
    response = client.post('/register/', data='http://example.com')
    assert response.status_code == 200
    assert db.session.query(Endpoint).count() == 1


def test_register_twice(db):
    client = app.test_client()
    response = client.post('/register/', data='http://example.com')
    response = client.post('/register/', data='http://example.net')
    assert response.status_code == 200
    assert db.session.query(Endpoint).count() == 2


def test_register_duplicate(db):
    client = app.test_client()
    response = client.post('/register/', data='http://example.com')
    response = client.post('/register/', data='http://example.com')
    assert response.status_code == 200
    assert db.session.query(Endpoint).count() == 1


def test_register_bad_data():
    client = app.test_client()
    response = client.post('/register/')
    assert response.status_code == 400


def test_list():
    client = app.test_client()
    response = client.post('/register/', data='http://example.com')
    reference = response.get_data()

    response = client.get('/list/')
    assert response.get_data() == '{}: {}\n'.format(
        reference, 'http://example.com')
