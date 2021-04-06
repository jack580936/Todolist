import pytest
from main import app, db, Todo


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='function')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert todolist data
    list1 = Todo(content='babachichi', status=4, done=False)
    list2 = Todo(content='hahahaha', status=3, done=True)
    db.session.add(list1)
    db.session.add(list2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    Todo.query.delete()
    db.session.commit()
    # db.drop_all() #刪除全部 連table都刪除
