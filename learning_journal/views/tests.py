"""Test my learning journal."""

import pytest
from pyramid import testing
import sys


@pytest.fixture()
def testapp():
    """Create an instance of our app for testing."""
    from learning_journal_basic import main
    app = main({})
    from webtest import TestApp
    return TestApp(app)


# =============Functional Tests===============

def test_layout_root(testapp):
    """Test that the contents of the root page contain expected text."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Learning Blog' in html.find("h1").text


def test_update_page_renders_file_data(testapp):
    """Ensure a detail pages exists."""
    response = testapp.get('/journal/0', status=200)
    assert 'lecture was difficult' in str(response.html)


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
