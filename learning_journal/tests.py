import pytest
import transaction
from pyramid import testing
from learning_journal.models.mymodel import Entry
from learning_journal.models.meta import Base
import sys



# ========== Unit Tests============


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


def test_entry_gets_added(db_session):
    """Test that entries are added to session."""
    entry1 = Entry(title='test_title1', body='test_body1', creation_date='test_date1')
    entry2 = Entry(title='test_title2', body='test_body2', creation_date='test_date2')
    entry3 = Entry(title='test_title3', body='test_body3', creation_date='test_date3')
    entry4 = Entry(title='test_title4', body='test_body4', creation_date='test_date4')
    for entry in (entry1, entry2, entry3, entry4):
        db_session.add(entry)
    assert db_session.query(Entry).count() == 4


def test_entry_attributes(db_session):
    """Test that new attributes are entered correctly."""
    entry1 = Entry(title='test_title1', body='Testing123', creation_date='test_date1')
    db_session.add(entry1)
    test_row = db_session.query(Entry).first()
    assert test_row.body == 'Testing123'


# =============Functional Tests===============


@pytest.fixture()
def testapp():
    """Create an instance of our app for testing."""
    from pyramid.config import Configurator
    from learning_journal.scripts.initializedb import ENTRIES
    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.scan()
        return config.make_wsgi_app()
    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    SessionFactory = app.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)
    from webtest import TestApp
    return TestApp(app)


def test_layout_root(testapp):
    """Test that the contents of the root page contain expected text."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Learning Blog' in html.find("h1").text


def test_update_page_renders_file_data(testapp):
    """Ensure a detail pages exists."""
    response = testapp.get('/journal/1', status=200)
    assert 'Jordan Schatzman' in str(response.html)


def test_multiple_edit_entry_page_exists(testapp):
    """Test that multiple journal pages exist."""
    response = testapp.get("/journal/2/edit-entry", status=200)
    html = response.html
    assert 'Submit' in str(response.html)


def test_create_new_page_exists(testapp):
    """Test that the create new page exists."""
    response = testapp.get("/journal/new-entry", status=200)
    assert 'New Journal' in str(response.html)


def test_for_home_link_in_detail(testapp):
    """Test home page link exists in detail page."""
    response = testapp.get('/journal/0', status=200)
    html = response.html
    """ There should be one link that is not a link to specific article."""
    assert '<a href="/">Home</a>' in map(str, html.findAll("a"))


def test_for_home_link_in_update(testapp):
    """Test home page link exists in detail page."""
    response = testapp.get('/journal/1/edit-entry', status=200)
    html = response.html
    """ There should be one link that is not a link to specific article."""
    assert '<a href="/">Home</a>' in map(str, html.findAll("a"))


def test_for_home_link_in_new(testapp):
    """Test home page link exists in create new page page."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    """ There should be one link that is not a link to specific article."""
    assert '<a href="/">Home</a>' in map(str, html.findAll("a"))
