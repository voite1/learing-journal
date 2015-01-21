from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import EntryFactory

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
   
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Updated in class to add security
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy('secret'),
        authorization_policy=ACLAuthorizationPolicy(),
        default_permission='view'
    )

    # ... Add the factory keyword argument to our route configurations:
    config.add_route('home', '/', factory=EntryFactory)
    config.add_route('detail', '/journal/{id:\d+}', factory=EntryFactory)
    config.add_route('action', '/journal/{action}', factory=EntryFactory)
    config.add_route('auth', '/sign/{action}', factory=EntryFactory)

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('home', '/')
    # config.add_route('detail', '/journal/{id:\d+}')
    # config.add_route('action', '/journal/{action}')
    config.scan()
    return config.make_wsgi_app()
