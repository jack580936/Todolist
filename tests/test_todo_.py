from app import create_app, db
from app.models import Todo


def test_index_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('default')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'HELLO Stranger!' in response.data


def test_index_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'HELLO Stranger!' in response.data
    response = test_client.get('/jack')
    # print(response.data)
    assert response.status_code == 200
    assert b'HELLO jack!' in response.data


def test_index_page_button(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    # print(response.data)
    assert response.status_code == 200
    assert b'HELLO Stranger!' in response.data
    assert b'The local date and time is' in response.data
    assert b'TODO App' in response.data
    assert b'Task name' in response.data
    assert b'Task deadline' in response.data
    assert b'Add task' in response.data


def test_index_post(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/update' page is requested (post)
    THEN check the response is valid
    THEN check the content and the status will be change
    """

    response = test_client.post('/', data={"content": "88777", "status": 0})
    print(response)
    assert Todo.query.get(3).content == "88777"
    assert Todo.query.get(3).status == 0


def test_create(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/create')
    print(response.json)

    assert response.status_code == 200
    assert response.json == {"result": True}
    query = Todo.query.filter_by(content='First_Record').first()
    db.session.delete(query)
    db.session.commit()


def test_read(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/read' page is requested (GET)
    THEN check the response is not none
    """
    response = test_client.get('/read')
    print(response.json)

    assert response.status_code == 200
    assert response.json is not None


def test_read_by_status(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/read' page is requested (GET)
    THEN check the response is not none
    """
    response = test_client.get('/read_by_status')
    print(response.json)

    assert response.status_code == 200
    assert response.json is not None


def test_search(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/search/<search_name>' page is requested (GET)
    THEN check the response is not none
    """
    response = test_client.get('/search/babachichi')
    print(response.json)
    response2 = test_client.get('/search/hahahaha')
    response3 = test_client.get('/search/abcdefgh')
    assert response.status_code == 200
    assert response.json is not None
    assert response2.json is not None
    assert response3.json == "NOT FOUND"


def test_search_post(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/search' page is requested (post)
    THEN check the response is valid
    THEN check the content and the status will be search
    """

    response = test_client.post('/search', data={"target": "babachichi"})
    print(response.data)
    assert b'babachichi' in response.data


def test_update(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/update' page is requested (GET)
    THEN check the response is valid
    THEN check the content and the status will be change
    """

    test_client.post('/update/1', data={"content": "5678", "status": 2})
    # print(response)
    assert Todo.query.get(1).content == "5678"
    assert Todo.query.get(1).status == 2


def test_delete(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/delete/2' page is requested (GET)
    THEN check list2 is not exist
    """
    response = test_client.get('/delete/2')

    assert response.status_code == 302
    assert Todo.query.get(1) is not None
    assert Todo.query.get(2) is None


def test_done(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/done/1' page is requested (GET)
    THEN check done_status is True
    WHEN the '/done/2' page is requested (GET)
    THEN check done_status is False
    """
    response = test_client.get('/done/1')
    test_client.get('/done/2')
    assert response.status_code == 302
    assert Todo.query.get(1).done is True
    assert Todo.query.get(2).done is False
