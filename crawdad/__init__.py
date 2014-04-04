"""Main entry point
"""
from pyramid.config import Configurator
from sqlalchemy import create_engine
from models import initialize_sql

db_name = "spacehub"

db_url = "sqlite:////tmp/test.db"


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("crawdad.views")
    engine = create_engine(db_url)
    initialize_sql(engine)
    return config.make_wsgi_app()
