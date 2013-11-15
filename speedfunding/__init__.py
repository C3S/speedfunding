from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = session_factory_from_settings(settings)

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          session_factory=session_factory,)
    config.include('pyramid_chameleon')
    config.add_subscriber('speedfunding.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('speedfunding.subscribers.add_locale_to_cookie',
                          'pyramid.events.NewRequest')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('speedfund', '/')
    config.scan()
    return config.make_wsgi_app()
