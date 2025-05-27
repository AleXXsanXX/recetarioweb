from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from recetarioweb.security import obtener_usuario_logueado

@view_config(context=HTTPNotFound, renderer="templates/404.jinja2")
def notfound_view(request):
    usuario_logueado = obtener_usuario_logueado(request)
    return {"usuario_logueado": usuario_logueado}

