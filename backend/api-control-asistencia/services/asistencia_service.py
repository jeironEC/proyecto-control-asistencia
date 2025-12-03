# Importaciones
from sqlmodel import Session, select
from models.Asistencias import Asistencia
from schemas.asistencia import CreaAsistencia, ActualizaAsistencia

def crear_asistencia(asistencia: CreaAsistencia, db: Session):
    """
    Crea una nueva asistencia

    Argumentos:
        asistencia (CreaAsistencia): Datos de la asistencia a crear
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Asistencia: Asistencia creada
    """
    db_asistencia = Asistencia(
        fecha=asistencia.fecha,
        hora=asistencia.hora,
        estado=asistencia.estado,
        usuario_id=asistencia.usuario_id,
    )

    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

def obtener_asistencias(db: Session):
    """
    Obtiene todas las asistencias

    Argumentos:
        db (Session): Sesion de la base de datos
    
    Devuelve:
        list[Asistencia]: Lista de asistencias
    """
    consulta_asistencias = select(Asistencia)
    resultados = db.exec(consulta_asistencias).all()

    return resultados

def obtener_asistencia_id(id: int, db: Session):
    """
    Obtiene una asistencia por su ID

    Argumentos:
        id (int): ID de la asistencia
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Asistencia: Asistencia encontrada
    """
    consulta_asistencia = select(Asistencia).where(Asistencia.id == id)
    resultado = db.exec(consulta_asistencia).first()

    return resultado

def actualizar_asistencia(id: int, datos: ActualizaAsistencia, db: Session):
    """
    Actualiza una asistencia

    Argumentos:
        id (int): ID de la asistencia
        datos (ActualizaAsistencia): Datos de la asistencia a actualizar
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Asistencia: Asistencia actualizada
    """
    asistencia = db.get(Asistencia, id)

    if not asistencia:
        return None
    
    datos_asistencia = datos.model_dump(exclude_unset=True)
    asistencia.sqlmodel_update(datos_asistencia)

    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)

    return asistencia

def eliminar_asistencia(id: int, db: Session):
    """
    Elimina una asistencia

    Argumentos:
        id (int): ID de la asistencia
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Asistencia: Asistencia eliminada
    """
    asistencia = db.get(Asistencia, id)

    if not asistencia:
        return None
    
    db.delete(asistencia)
    db.commit()
    return asistencia