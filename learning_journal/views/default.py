import os
from pyramid.view import view_config
from datetime import date as Date
from pyramid.httpexceptions import HTTPFound
from ..models import Entry
from learning_journal.security import check_credentials
from pyramid.security import remember, forget
from pyramid.security import NO_PERMISSION_REQUIRED

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


@view_config(route_name='create', renderer='templates/new_entry.jinja2', permission='create')
def create_view(request):
    """Create new view handler."""
    if request.method == "POST":
        today = Date.today()
        title = request.POST['title']
        body = request.POST['body']
        creation_date = "{}-{}-{}".format(today.year, today.month, today.day)
        entry = Entry(title=title, body=body, creation_date=creation_date)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    if request.method == "GET":
        today = Date.today()
        return {"creation_date": "{}-{}-{}".format(today.year, today.month, today.day)}


@view_config(route_name='update', renderer='templates/update.jinja2', permission='edit')
def update_view(request):
    """Update/edit view handler."""
    if request.method == 'GET':
        entry = request.dbsession.query(Entry).filter_by(id=request.matchdict['id']).first()
        return {'entries': entry}
    elif request.method == 'POST':
        entry = request.dbsession.query(Entry).get(request.matchdict['id'])
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        return HTTPFound(location=request.route_url('home'))


@view_config(route_name='login',renderer='../templates/login.jinja2', permission=NO_PERMISSION_REQUIRED)
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(location=request.route_url('home'),
                             headers=auth_head)
    return {} 


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
