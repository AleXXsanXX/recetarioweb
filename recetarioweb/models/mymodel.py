from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(Unicode(50), unique=True, nullable=False)
    email = Column(Unicode(100), unique=True, nullable=False)
    contraseña = Column(Unicode(128), nullable=False)
    foto_perfil = Column(Unicode(255))

    recetas = relationship("Receta", back_populates="autor", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")


class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True)
    titulo = Column(Unicode(100), nullable=False)
    descripcion = Column(UnicodeText)
    imagen = Column(Unicode(255))
    ingredientes = Column(UnicodeText) 
    instrucciones = Column(UnicodeText)
    fecha = Column(DateTime, server_default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    autor = relationship("Usuario", back_populates="recetas")
    comentarios = relationship("Comentario", back_populates="receta", cascade="all, delete-orphan")


class Comentario(Base):
    __tablename__ = 'comentarios'
    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    receta_id = Column(Integer, ForeignKey('recetas.id'))

    usuario = relationship("Usuario", back_populates="comentarios")
    receta = relationship("Receta", back_populates="comentarios")
