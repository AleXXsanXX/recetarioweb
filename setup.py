from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'zope.sqlalchemy',
    'transaction',
    'waitress',
    'alembic',
    # cualquier otra dependencia que tuvieras
]

setup(
    name='recetarioweb',
    version='0.1',
    description='Recetario Web project',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = recetarioweb:main',
        ],
    },
)
