import os
from pyramid.view import view_config

THIS_DIR = os.path.dirname(__file__)


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    """Home view handler."""
    return {"entries": ENTRIES}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    """Detail view handler."""
    entry_id = int(request.matchdict['id'])
    return {'entries': ENTRIES[entry_id]}


@view_config(route_name='create', renderer='templates/new_entry.jinja2')
def create_view(request):
    """Create new view handler."""
    return {}


@view_config(route_name='update', renderer='templates/update.jinja2')
def update_view(request):
    """Update/edit view handler."""
    entry_id = int(request.matchdict['id'])
    return {'entries': ENTRIES[entry_id]}