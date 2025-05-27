import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Si no existen README.txt o CHANGES.txt, Render puede fallar, así que usa texto por defecto
README = open(os.path.join(here, 'README.txt'), encoding='utf-8').read() if os.path.exists('README.txt') else ''
CHANGES = open(os.path.join(here, 'CHANGES.txt'), encoding='utf-8').read() if os.path.exists('CHANGES.txt') else ''

requires = [
    'alembic',
    'plaster_pastedeploy',
    'pyramid >= 1.9',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'PyMySQL',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1',
    'pytest>=3.7.4',
    'pytest-cov',
]

setup(
    name='recetarioweb',
    version='0.1',
    description='Recetario Web',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(where='.'),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = recetarioweb:main',
        ],
        'console_scripts': [
            'initialize_recetarioweb_db = recetarioweb.scripts.initialize_db:main',
        ],
    },
)
