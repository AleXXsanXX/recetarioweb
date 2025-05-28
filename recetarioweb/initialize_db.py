from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from recetarioweb.models.mymodel import Base
import os

if __name__ == "__main__":
    settings = get_appsettings("production.ini")  # Asegúrate de que production.ini esté en tu raíz del proyecto
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
