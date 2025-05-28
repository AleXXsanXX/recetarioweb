from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from recetarioweb.models.mymodel import Usuario


def get_user(request):
    user_id = request.authenticated_userid
    if user_id:
        return request.dbsession.query(Usuario).get(int(user_id))
    return None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    with Configurator(settings=settings) as config:
        
        authn_policy = AuthTktAuthenticationPolicy('mi_clave_super_secreta_123', hashalg='sha512') # Usa una clave secreta única
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)
        
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('recetarioweb:templates')
        config.include('.models')
        config.include('.security')
        config.include('.routes')  # Ya maneja todas las rutas
        
        #rutas
        config.add_route('home', '/')
        config.add_route('recetas', '/recetas')  #  ESTA es la que usas en tu view_config
        config.add_route('mis_recetas', '/recetas/mias')
        config.add_route('todas_recetas', '/recetas/todas')
        config.add_route('agregar_receta', '/recetas/agregar')
        config.add_route('ver_receta', '/recetas/{id}')
        config.add_route('editar_receta', '/recetas/{id}/editar')
        config.add_route('eliminar_receta', '/recetas/{id}/eliminar')
        config.add_route('agregar_comentario', '/recetas/{id}/comentarios')
        config.add_route('eliminar_comentario', '/comentarios/{id}/eliminar')
        config.add_route('registro', '/registro')
        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        


        session_factory = SignedCookieSessionFactory(settings['session.secret'])
        config.set_session_factory(session_factory)
        config.add_static_view(name='static', path='recetarioweb:static', cache_max_age=3600)

        config.add_request_method(get_user, 'user', reify=True)
        
        config.scan()
        from sqlalchemy import engine_from_config
        from recetarioweb.models.meta import Base 
        engine = engine_from_config(settings, 'sqlalchemy.')
        Base.metadata.create_all(engine)

    return config.make_wsgi_app()
