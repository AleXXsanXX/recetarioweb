from setuptools import setup, find_packages

setup(
    name='recetarioweb',
    version='0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyramid',
        'SQLAlchemy',
        'zope.sqlalchemy',
        'pyramid_jinja2',
        'alembic',
        'waitress',
        'bcrypt'
    ],
    entry_points={
        'paste.app_factory': [
            'main = recetarioweb:main',
        ],
    },
)

