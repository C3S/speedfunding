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
    config.add_static_view('static_deform', 'deform:static')
    config.add_subscriber('speedfunding.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('speedfunding.subscribers.add_locale_to_cookie',
                          'pyramid.events.NewRequest')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('speedfund', '/')  # the landing page
    config.add_route('donate', '/donate')
    config.add_route('shirt', '/shirt')
    config.add_route('success', '/success')
    config.add_route('yes', '/yes')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('total', '/total')
    config.add_route('dashboard', '/dashboard/{number}')
    config.add_route('detail', '/detail/{speed_id}')
    config.add_route('switch_pay', '/switch_pay/{speed_id}')
    config.add_route('delete_entry', '/delete/{speed_id}')
    config.scan()
    return config.make_wsgi_app()
