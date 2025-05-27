def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('agregar_receta', '/recetas/nueva')
    config.add_route('ver_receta', '/recetas/{id}')
    config.add_route('agregar_comentario', '/comentarios/agregar/{receta_id}')
    config.add_route('eliminar_receta', '/recetas/{id}/eliminar')
    config.add_route('editar_receta', '/recetas/{id}/editar')
    config.add_route('eliminar_comentario', '/comentarios/{id}/eliminar')





