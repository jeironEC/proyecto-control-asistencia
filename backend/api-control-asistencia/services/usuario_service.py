# Importaciones
from sqlmodel import Session, select
from models.Usuarios import Usuario
from models.Asistencias import Asistencia
from schemas.usuario import CreaUsuario, ActualizaUsuario
from core.security import cifrar_contrasena, contrasena_contexto
from datetime import date

def crear_usuario(usuario: CreaUsuario, db: Session):
    """
    Crea un nuevo usuario

    Argumentos:
        usuario (CreaUsuario): Datos del usuario a crear
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario creado
    """
    contrasena_cifrada = cifrar_contrasena(usuario.contrasena)

    inserta_usuario = Usuario(
        nombre =  usuario.nombre,
        apellido =  usuario.apellido,
        correo =  usuario.correo,
        contrasena =  contrasena_cifrada,
        rol = usuario.rol,
        activo = usuario.activo
    )

    db.add(inserta_usuario)
    db.commit()
    db.refresh(inserta_usuario)
    return inserta_usuario

def obtener_usuario_id(id: int, db: Session):
    """
    Obtiene un usuario por su ID

    Argumentos:
        id (int): ID del usuario
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario encontrado
    """
    consulta_usuario = select(Usuario).where(Usuario.id == id)
    resultado = db.exec(consulta_usuario).first()

    return resultado

def obtener_usuario_correo(correo: str, db: Session):
    """
    Obtiene un usuario por su correo

    Argumentos:
        correo (str): Correo del usuario
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario encontrado
    """
    consulta_usuario = select(Usuario).where(Usuario.correo == correo)
    resultado = db.exec(consulta_usuario).first()

    return resultado 

def obtener_usuarios(db: Session):
    """
    Obtiene todos los usuarios

    Argumentos:
        db (Session): Sesion de la base de datos
    
    Devuelve:
        list[Usuario]: Lista de usuarios
    """
    consulta_usuarios = select(Usuario)
    resultados = db.exec(consulta_usuarios).all()

    return resultados

def verificar_contrasena(contrasena, contrasena_hashed):
    """
    Verifica si una contrasena es correcta comparando la contrasena con la contrasena hasheada

    Argumentos:
        contrasena (str): Contraseña a verificar
        contrasena_hashed (str): Contraseña hasheada
    
    Devuelve:
        bool: True si la contrasena es correcta, False en caso contrario
    """
    return contrasena_contexto.verify(contrasena, contrasena_hashed)

def obtener_hash_contrasena(password):
    """
    Obtiene un hash de una contrasena

    Argumentos:
        password (str): Contraseña a hashear
    
    Devuelve:
        str: Contraseña hasheada
    """
    return contrasena_contexto.hash(password)

def actualizar_estado_usuario(id: int, db: Session):
    """
    Actualiza el estado de un usuario

    Argumentos:
        id (int): ID del usuario
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario actualizado
    """
    usuario = obtener_usuario_id(id, db)

    if not usuario:
        return None

    usuario.activo = not usuario.activo

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario

def actualizar_usuario(id: int, datos: ActualizaUsuario, db: Session):
    """
    Actualiza un usuario

    Argumentos:
        id (int): ID del usuario
        datos (ActualizaUsuario): Datos del usuario a actualizar
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario actualizado
    """
    usuario = db.get(Usuario, id)

    if not usuario: 
        return None
    
    datos_usuario = datos.model_dump(exclude_unset=True)
    usuario.sqlmodel_update(datos_usuario)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario

def eliminar_usuario(id: int, db: Session):
    """
    Elimina un usuario

    Argumentos:
        id (int): ID del usuario
        db (Session): Sesion de la base de datos
    
    Devuelve:
        bool: True si el usuario se elimino correctamente, False en caso contrario
    """
    usuario = db.get(Usuario, id)

    if not usuario:
        return None
    
    db.delete(usuario)
    db.commit()

    return True

def obtener_rango_asistencias_usuario(id: int, fecha_inicial: date, fecha_final: date, db: Session):
    """
    Obtiene un rango de asistencias de un usuario

    Argumentos:
        id (int): ID del usuario
        fecha_inicial (date): Fecha inicial
        fecha_final (date): Fecha final
        db (Session): Sesion de la base de datos
    
    Devuelve:
        list[Asistencia]: Lista de asistencias
    """
    consulta = select(Asistencia).where(Asistencia.usuario_id == id, Asistencia.fecha.between(fecha_inicial, fecha_final))
    resultados = db.exec(consulta).all()

    return resultados