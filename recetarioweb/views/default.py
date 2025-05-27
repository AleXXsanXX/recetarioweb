from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import Usuario

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    user_id = request.authenticated_userid

    if user_id:
        usuario = request.dbsession.query(Usuario).get(user_id)
        if usuario:
            # ✅ Usuario autenticado: ir a la página informativa
            return HTTPFound(location=request.route_url('recetas'))

    # ✅ Usuario NO autenticado: mostrar el home real (templates/home.jinja2)
    return {}


