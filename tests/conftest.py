import os

import pytest


def pytest_configure(config):
    # make sure we use in-memory sqlite
    os.environ['DB_URI'] = 'sqlite://'


@pytest.fixture
def db():
    from adyen_notification_proxy.models import db, Endpoint
    db.create_all()
    db.session.query(Endpoint).delete()
    return db
