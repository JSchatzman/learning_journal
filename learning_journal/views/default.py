import os
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import Entry

THIS_DIR = os.path.dirname(__file__)


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    """Home view handler."""
    entries = request.dbsession.query(Entry).order_by(-Entry.id).all()
    entry_list = []
    for entry in entries:
        entry_list.append(entry)
    return {'entries': entry_list}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    """Detail view handler."""
    entry = request.dbsession.query(Entry).filter_by(id=request.matchdict['id']).first()
    return {'entries': entry}


@view_config(route_name='create', renderer='templates/new_entry.jinja2')
def create_view(request):
    """Create new view handler."""
    return {}


@view_config(route_name='update', renderer='templates/update.jinja2')
def update_view(request):
    """Update/edit view handler."""
    entry = request.dbsession.query(Entry).filter_by(id=request.matchdict['id']).first()
    if request.method == 'GET':
        return {'entries': entry}
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        entry = Entry(title=title, body=body, creation_date=entry.creation_date)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('home'))
