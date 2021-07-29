

### tests to do:

###test length of session is correct
###test elo grossly (three people, make sure a wins all and has highest elo
###test actually going through it
###test number of docs in database
###test pure function types generate
###test g
###test session

import os
import pytest


@pytest.fixture
def app():
    from main import app

    #app.config["TESTING"] = True
    app.testing = True
    app.config['SECRET_KEY'] = 'my secret key'
    app.config['DATABASE_NAME'] = 'test_database'

    with app.app_context():
        print(app)

    yield app


@pytest.fixture(scope="session")
def some_resource(request):
    print('\nSome resource')

    def some_resource_fin():
        print('\nSome resource fin')

    request.addfinalizer(some_resource_fin)


@pytest.fixture
def get_app():
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
