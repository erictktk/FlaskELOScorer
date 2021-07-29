"""def test_config():
    print('app.testing = ' + str(app.testing))
    assert app.testing == True
"""
import time

import pymongo
from pymongo import mongo_client
import werkzeug

import flask
from flask import g


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'


def test_session_lengths(some_resource, client):
    response = client.get('/vibes-initiate')

    with client.session_transaction() as session:
        print(len(session['types']))
        assert len(session['types']) >= 50
        assert len(session['types']) <= 80


def test_initiate_session(some_resource, client):
    response = client.get('/vibes-initiate')

    time.sleep(.1)

    ### session_transaction allows you to modify session
    ###“session transaction” which simulates the appropriate calls to open a session in the context of the test client and to modify it
    ###

    with client.session_transaction() as session:
        print(session)
        assert session['inSession']

    assert response.status_code == 302

    db = g.db  # type: mongo_client.database
    db = db  # type: mongo_client.database

    assert g.db is not None
    assert db.name == "test_db"

    ## g.db can also be used with
    #with app.test_request_context('/url'):
    #    app
    #   app.preprocess_request()  for before_request functions //these might be covered by fixtures

    # https://flask.palletsprojects.com/en/2.0.x/testing/#other-testing-tricks

    #client.post()


def test_iter(app, client):
    response = client.get('/vibes-initiate')

    #request.headers


def test_session_timeout(app, client):
    #headers = werkzeug.datastructures.Headers()

    headers = {'time'}

    import datetime
    now = datetime.datetime.now()
    now = now + datetime.timedelta(minutes=11)  # date of 11 minutes later

    """
    #can be used for session, g and request
    with app.test_request_context(
            '/vibes-initiate', data={'format': 'short'}):
        generate_report()
    """
    ###
    ### https://flask.palletsprojects.com/en/2.0.x/reqcontext/
    ###

    ###
    ### session['inSession'] = True
    ### session['types'] = types
    ### session['startTime'] = datetime.datetime.now()



    response = client.get('/vibes-initiate')

    time.sleep(.1)
    assert response.status_code == 302
    assert g.db is not None

    response = client.get('/vibes-session', query_string={'curiter': '0'})
    assert g.cur_iter == 0

    """
    with app.test_request_context('/vibes-session?curiter=1') as response:
        assert response.status_code == "302"


    class NewDate(datetime.date):
        @classmethod
        def now(cls):
            return now

    datetime.date = NewDate

    from urllib.parse import urlparse

    with app.test_request_context('/vibes-sesion?curiter=0') as response:
        expectedPath = '/session-timeout'
        assert response.status_code == 302
        #self.assertEqual(urlparse(response.location).path, expectedPath)
        assert expectedPath == urlparse(response.location)
    """