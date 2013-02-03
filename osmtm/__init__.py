from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from .resources import (
    MapnikRendererFactory
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['mako.directories'] = 'osmtm:templates'

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('job_new', '/job/new')
    config.add_route('job', '/job/{job}')
    config.add_route('job_edit', '/job/{job}/edit')
    config.add_route('job_mapnik', '/job/{job}/{z}/{x}/{y}.{format}')

    config.add_renderer('mapnik', MapnikRendererFactory)

    config.scan()
    return config.make_wsgi_app()
