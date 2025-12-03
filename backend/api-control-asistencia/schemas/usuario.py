# Importaciones
from sqlmodel import SQLModel
from models.Usuarios import RolUsuario

class CreaUsuario(SQLModel):
    """
    Esquema para crear un nuevo usuario

    Argumentos:
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        correo (str): Correo del usuario
        contrasena (str): Contraseña del usuario
        rol (RolUsuario): Rol del usuario
        activo (bool): Estado del usuario
    
    Devuelve:
        CreaUsuario: Usuario creado
    """
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    rol: RolUsuario
    activo: bool

class ObtenUsuarios(SQLModel):
    """
    Esquema para obtener un usuario

    Argumentos:
        id (int): ID del usuario
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        correo (str): Correo del usuario
        rol (RolUsuario): Rol del usuario
        activo (bool): Estado del usuario
    
    Devuelve:
        ObtenUsuarios: Usuario obtenido
    """
    id: int
    nombre: str
    apellido: str
    correo: str
    rol: RolUsuario
    activo: bool

class ActualizaUsuario(SQLModel):
    """
    Esquema para actualizar un usuario

    Argumentos:
        nombre (str | None): Nombre del usuario
        apellido (str | None): Apellido del usuario
        correo (str | None): Correo del usuario
        contrasena (str | None): Contraseña del usuario
        rol (RolUsuario | None): Rol del usuario
        activo (bool | None): Estado del usuario
    
    Devuelve:
        ActualizaUsuario: Usuario actualizado
    """
    nombre: str | None = None
    apellido: str | None = None
    correo: str | None = None
    contrasena: str | None = None
    rol: RolUsuario | None = None
    activo: bool | None = None