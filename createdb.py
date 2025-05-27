import os
import sys
from sqlalchemy import engine_from_config
from recetarioweb.models import Base  # importa el Base que contiene tus modelos
from recetarioweb import models

from pyramid.paster import get_appsettings

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python createdb.py development.ini")
        sys.exit(1)

    config_uri = sys.argv[1]
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
    print("Tablas creadas correctamente.")
