# Importaciones
from sqlmodel import create_engine, Session
from core.config import DATABASE_URL

# Motor de base de datos
engine = create_engine(DATABASE_URL)

def obtener_db():
    """
    Funcion para obtener la conexion a la base de datos. Conexion eficente con la base de datos.

    Returns:
        Session: Sesion de la base de datos
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

    return db