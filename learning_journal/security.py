import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import SignedCookieSessionFactory


class MyRoot(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'edit'),
        (Allow, Authenticated, 'create'),
        (Allow, Everyone, 'view')

    ]


def check_credentials(username, password):
    if username and password:
        if username == os.environ['AUTH_USERNAME']:
            return pwd_context.verify(password, os.environ['AUTH_PASSWORD'])
    return False


def includeme(config):
    """Pyramid security configuration.."""
    auth_secret = os.environ.get('AUTH_SECRET', 'snakesforall')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512')
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(MyRoot)
    session_secret = os.environ.get('SESSION_SECRET', 'snakesforall')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    #config.set_default_csrf_options(require_csrf=True)
    pass