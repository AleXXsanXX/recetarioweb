from pyramid.view import view_config

@view_config(route_name='recetas', renderer='json')
def ver_recetas(request):
    return {"mensaje": "Aquí se mostrarán las recetas"}
