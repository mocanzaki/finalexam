from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator
import uuid


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.set_session_factory(SignedCookieSessionFactory(uuid.uuid4().hex))
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
