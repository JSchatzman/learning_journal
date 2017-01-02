import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from passlib.apps import custom_app_context as pwd_context



class MyRoot(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'add'),
    ]


def check_credentials(username, password):
    if username and password:
        if username == os.environ['AUTH_USERNAME']:
            return pwd_context.verify(password, os.environ['AUTH_PASSWORD'])
    return False
    # stored_username = os.environ.get('AUTH_USERNAME', '')
    # stored_password = os.environ.get('AUTH_PASSWORD', '')
    # is_authenticated = False
    # if stored_username and stored_password:
    #     if username == stored_username:
    #         if password == stored_password:
    #             is_authenticated = True
    # return is_authenticated



def includeme(config):
    """Pyramid security configuration.."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512')
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(MyRoot)