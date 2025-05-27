from recetarioweb.models.mymodel import Usuario

def obtener_usuario_logueado(request):
    user_id = request.authenticated_userid

    if user_id is None:
        return None

    try:
        return request.dbsession.query(Usuario).get(int(user_id))
    except (ValueError, TypeError):
        return None


def includeme(config):
    config.add_request_method(obtener_usuario_logueado, name='user', reify=True)
