import os
from recetarioweb import main
from pyramid.paster import get_appsettings

ini_path = os.path.join(os.path.dirname(__file__), '..', 'development.ini')

settings = get_appsettings(ini_path)

app = main({}, **settings)
