import pytest

from app import create_app
from app.modules.users.models import User
from app.modules.roles.models import Role
from tests import utils


@pytest.yield_fixture(scope='session')
def flask_app():
    app = create_app(config_name='testing')
    from app import db

    with app.app_context():
        db.create_all()
        user = User(email='test@test.com',
                    username='test',
                    first_name='Chaos',
                    last_name='Monkey',
                    password='password')
        db.session.add(user)
        role = Role(name='Admin',
                    description='All powerful')
        db.session.add(role)
        db.session.commit()
        yield app
        db.drop_all()


@pytest.yield_fixture(scope='session')
def db(flask_app):
    from app import db as db_instance
    yield db_instance
    db_instance.session.rollback()


@pytest.fixture(scope='session')
def flask_app_client(flask_app):
    flask_app.response_class = utils.JSONResponse
    return flask_app.test_client()
