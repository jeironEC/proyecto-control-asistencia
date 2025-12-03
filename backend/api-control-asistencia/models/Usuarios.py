# Importaciones
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, ForeignKey
from enum import Enum

class RolUsuario(Enum):
    """
    Enum para los roles de los usuarios que puede ser ALUMNO, PROFESOR o PERSONALSERVICIO

    Argumentos:
        ALUMNO (str): Rol de alumno
        PROFESOR (str): Rol de profesor
        PERSONALSERVICIO (str): Rol de personal de servicio

    Devuelve:
        RolUsuario: Enum con los roles de los usuarios
    """
    ALUMNO = "alumno"
    PROFESOR = "profesor"
    PERSONALSERVICIO = "personal_servicio"

class Usuario(SQLModel, table=True):
    """
    Modelo para los usuarios que contiene los siguientes campos:

    Campos:
        id (int): Id del usuario
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        correo (str): Correo del usuario
        contrasena (str): Contraseña del usuario
        rol (RolUsuario): Rol del usuario
        activo (bool): Estado del usuario
    """
    __tablename__ = "usuario"

    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    correo: str = Field(max_length=150, unique=True, index=True)
    contrasena: str
    rol: RolUsuario
    activo: bool = Field(default=1)