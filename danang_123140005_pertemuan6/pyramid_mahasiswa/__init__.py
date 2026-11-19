from pyramid.config import Configurator


def main(global_config, **settings):
    """Fungsi utama yang mengembalikan instance Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
