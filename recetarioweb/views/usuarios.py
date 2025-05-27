from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import IntegrityError
from pyramid.security import remember, forget
from passlib.hash import bcrypt
from ..models import Usuario
import os, uuid, shutil

RUTA_UPLOADS_USUARIOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'usuarios'))

@view_config(route_name='registro', renderer='templates/usuarios/registro.jinja2')
def registro_view(request):
    mensaje_error = ''

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')  # <- Cambiado
        imagen_archivo = request.POST.get('foto_perfil')  # cambiar más abajo

        if not nombre or not email or not password:
            mensaje_error = "Todos los campos son obligatorios"
        else:
            existente = request.dbsession.query(Usuario).filter(
                (Usuario.nombre == nombre) | (Usuario.email == email)
            ).first()

            if existente:
                mensaje_error = "Ese nombre de usuario o email ya está en uso"
            else:
                contrasena_segura = bcrypt.hash(password)
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    email=email,
                    contraseña=contrasena_segura
                )

                # archivo: acceder como objeto file
                imagen_archivo = request.POST['foto_perfil']
                if hasattr(imagen_archivo, 'file') and imagen_archivo.filename:
                    extension = os.path.splitext(imagen_archivo.filename)[1]
                    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
                    ruta_archivo = os.path.join(RUTA_UPLOADS_USUARIOS, nombre_archivo)

                    with open(ruta_archivo, 'wb') as f:
                        shutil.copyfileobj(imagen_archivo.file, f)

                    nuevo_usuario.foto_perfil = nombre_archivo

                request.dbsession.add(nuevo_usuario)
                request.dbsession.flush() # ✅ Esto garantiza que el ID esté asignado
                
                headers = remember(request, str(nuevo_usuario.id))  # ✅ ID garantizado
                return HTTPFound(location=request.route_url('home'), headers=headers)


    return {'error': mensaje_error}


@view_config(route_name='login', renderer='templates/usuarios/login.jinja2')
def login_view(request):
    mensaje_error = ''

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contrasena = request.POST.get('contrasena')

        usuario = request.dbsession.query(Usuario).filter_by(nombre=nombre).first()

        if usuario and bcrypt.verify(contrasena, usuario.contraseña):  # Correcto
            headers = remember(request, str(usuario.id))
            next_url = request.params.get('next') or request.route_url('home')
            return HTTPFound(location=next_url, headers=headers)  # <-- ✅ CORREGIDO


        else:
            mensaje_error = 'Nombre de usuario o contraseña incorrectos'

    return {'error': mensaje_error}


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    request.session.flash('Sesión cerrada correctamente.', 'info')
    return HTTPFound(location=request.route_url('login'), headers=headers)
