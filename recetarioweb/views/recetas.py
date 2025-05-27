from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
#from pyramid.security import authenticated_userid /no usar
import os
import uuid
import shutil
from ..models import Receta, Comentario, Usuario

RUTA_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'recetas'))


@view_config(route_name='recetas', renderer='../templates/recetas/ver_recetas.jinja2')
def ver_recetas(request):
    try:
        recetas = request.dbsession.query(Receta).all()
        return {'recetas': recetas}
    except:
        return Response("Error al acceder a la base de datos", content_type='text/plain', status=500)


@view_config(route_name='agregar_receta', renderer='templates/recetas/agregar_receta.jinja2', request_method=('GET', 'POST'))
def agregar_receta_view(request):
    usuario_id = request.authenticated_userid
    if not usuario_id:
        raise HTTPForbidden()

    mensaje_error = ''

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        ingredientes = request.POST.get('ingredientes')
        instrucciones = request.POST.get('instrucciones')
        nombre_archivo = None

        # Validación básica
        if not titulo or not descripcion or not ingredientes or not instrucciones:
            mensaje_error = 'Todos los campos son obligatorios'
        else:
            imagen_archivo = request.POST.get('imagen')

            if hasattr(imagen_archivo, 'file') and imagen_archivo.filename:
                extension = os.path.splitext(imagen_archivo.filename)[1]
                nombre_archivo = f"{uuid.uuid4().hex}{extension}"
                ruta_archivo = os.path.join(RUTA_UPLOADS, nombre_archivo)

                with open(ruta_archivo, 'wb') as f:
                    shutil.copyfileobj(imagen_archivo.file, f)

            nueva_receta = Receta(
                titulo=titulo,
                descripcion=descripcion,
                ingredientes=ingredientes,
                instrucciones=instrucciones,
                imagen=nombre_archivo,
                usuario_id=usuario_id
            )

            request.dbsession.add(nueva_receta)
            return HTTPFound(location=request.route_url('recetas'))

    return {'error': mensaje_error}


@view_config(route_name='recetas', renderer='../templates/recetas/ver_recetas.jinja2')
def ver_recetas(request):
    usuario_id = request.authenticated_userid
    if not usuario_id:
        raise HTTPFound(location=request.route_url('home'))

    try:
        usuario = request.dbsession.query(Usuario).get(int(usuario_id))
        recetas = request.dbsession.query(Receta).order_by(Receta.id.desc()).all()
        return {
            'recetas': recetas,
            'usuario_logueado': usuario
        }
    except:
        return Response("Error al acceder a la base de datos", content_type='text/plain', status=500)




@view_config(route_name='ver_receta', renderer='../templates/recetas/ver_receta.jinja2')
def ver_receta_view(request):
    receta_id = request.matchdict.get('id')
    receta = request.dbsession.query(Receta).get(int(receta_id))

    if not receta:
        raise HTTPNotFound("Receta no encontrada.")

    usuario_id = request.authenticated_userid
    usuario = request.dbsession.query(Usuario).get(int(usuario_id)) if usuario_id else None

    return {
        'receta': receta,
        'usuario_logueado': usuario
    }




@view_config(route_name='agregar_comentario', request_method='POST')
def agregar_comentario_view(request):
    usuario_id = request.authenticated_userid  # ✅ esta es la forma correcta
    if not usuario_id:
        raise HTTPForbidden()

    receta_id = request.matchdict.get('id')
    contenido = request.POST.get('contenido', '').strip()

    if not contenido:
        request.session.flash('El comentario no puede estar vacío.', 'error')
        return HTTPFound(location=request.route_url('ver_receta', id=receta_id))

    nuevo_comentario = Comentario(
        contenido=contenido,
        usuario_id=usuario_id,
        receta_id=receta_id
    )
    request.dbsession.add(nuevo_comentario)
    request.session.flash('Comentario agregado correctamente.')
    return HTTPFound(location=request.route_url('ver_receta', id=receta_id))


@view_config(route_name='eliminar_receta', request_method='POST')
def eliminar_receta_view(request):
    usuario_id = request.authenticated_userid  # ✅ esta es la forma correcta
    if not usuario_id:
        raise HTTPForbidden()

    receta_id = request.matchdict.get('id')
    receta = request.dbsession.query(Receta).filter_by(id=receta_id).first()

    if not receta:
        raise HTTPNotFound("Receta no encontrada")

    if receta.usuario_id != int(usuario_id):
        raise HTTPForbidden()

    request.dbsession.delete(receta)
    request.session.flash('Receta eliminada correctamente.')
    return HTTPFound(location=request.route_url('recetas'))


@view_config(route_name='editar_receta', renderer='templates/recetas/editar_receta.jinja2')
def editar_receta_view(request):
    usuario_id = request.authenticated_userid  # ✅ esta es la forma correcta
    if not usuario_id:
        raise HTTPForbidden()

    receta_id = int(request.matchdict.get('id'))
    receta = request.dbsession.query(Receta).filter_by(id=receta_id).first()
    if not receta:
        raise HTTPNotFound()

    if receta.usuario_id != int(usuario_id):
        raise HTTPForbidden()

    if request.method == 'POST':
        receta.titulo = request.POST.get('titulo')
        receta.descripcion = request.POST.get('descripcion')
        receta.ingredientes = request.POST.get('ingredientes')
        receta.instrucciones = request.POST.get('instrucciones')

        if request.POST.get('eliminar_imagen') and receta.imagen:
            try:
                os.remove(os.path.join(RUTA_UPLOADS, receta.imagen))
            except FileNotFoundError:
                pass
            receta.imagen = None

        imagen_archivo = request.POST.get('imagen')
        if hasattr(imagen_archivo, 'filename') and imagen_archivo.filename:
            extension = os.path.splitext(imagen_archivo.filename)[1]
            nuevo_nombre = f"{uuid.uuid4().hex}{extension}"
            ruta_archivo = os.path.join(RUTA_UPLOADS, nuevo_nombre)

            if receta.imagen:
                try:
                    os.remove(os.path.join(RUTA_UPLOADS, receta.imagen))
                except FileNotFoundError:
                    pass

            with open(ruta_archivo, 'wb') as f:
                shutil.copyfileobj(imagen_archivo.file, f)

            receta.imagen = nuevo_nombre

        return HTTPFound(location=request.route_url('ver_receta', id=receta.id))

    return {'receta': receta}


@view_config(route_name='eliminar_comentario', request_method='GET')
def eliminar_comentario_view(request):
    usuario_id = request.authenticated_userid  # ✅ esta es la forma correcta
    if not usuario_id:
        raise HTTPForbidden()

    comentario_id = request.matchdict.get('id')
    comentario = request.dbsession.query(Comentario).get(comentario_id)

    if not comentario:
        raise HTTPNotFound()

    if comentario.usuario_id != int(usuario_id):
        raise HTTPForbidden()

    receta_id = comentario.receta_id
    request.dbsession.delete(comentario)
    request.session.flash('Comentario eliminado correctamente.')

    return HTTPFound(location=request.route_url('ver_receta', id=receta_id))


@view_config(route_name='todas_recetas', renderer='../templates/recetas/todas_recetas.jinja2')
def ver_todas_recetas_view(request):
    recetas = request.dbsession.query(Receta).all()
    usuario_id = request.authenticated_userid
    usuario = request.dbsession.query(Usuario).get(int(usuario_id)) if usuario_id else None

    return {
        'recetas': recetas,
        'usuario_logueado': usuario
    }

@view_config(route_name='mis_recetas', renderer='../templates/recetas/mis_recetas.jinja2')
def mis_recetas_view(request):
    usuario = request.user

    if usuario is None:
        return HTTPFound(location=request.route_url('login'))

    recetas = request.dbsession.query(Receta).filter_by(usuario_id=usuario.id).all()

    return {
        'recetas': recetas,
        'usuario_logueado': usuario,  # <- aquí corregido
    }
