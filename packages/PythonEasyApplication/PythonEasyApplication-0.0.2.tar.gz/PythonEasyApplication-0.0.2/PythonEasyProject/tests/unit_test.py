from PythonEasyProject.app import app

def test_hello_world():
    client = app.test_client()
    response = client.get('/')
    assert b"Welcome to the Python Easy Project" in response.data

def test_message_from_backend():
    client = app.test_client()
    response = client.get('/')
    assert b"Message from the back-end: LEMON!" in response.data
