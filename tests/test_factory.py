from flaskr import create_app


def test_config():
    print('test config')
    assert not create_app().testing
    assert create_app({'TESTING': False}).testing


def test_hello(client):
    print('test hello')
    response = client.get('/hello')
    assert response.data == b'Hello World!'
