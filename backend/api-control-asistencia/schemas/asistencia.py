# Importaciones
from sqlmodel import SQLModel
from datetime import date, time
from models.Asistencias import EstadoAsistencia

class CreaAsistencia(SQLModel):
    """
    Esquema para crear una nueva asistencia que contiene el fecha, hora_inicio, hora_fin, estado, modulo_id y usuario_id
    """
    fecha: date
    hora: time
    estado: EstadoAsistencia
    usuario_id: int

class ObtenAsistencias(SQLModel):
    """
    Esquema para obtener una asistencia que contiene el id, fecha, hora_inicio, hora_fin, estado, modulo_id y usuario_id
    """
    id: int
    fecha: date
    hora: time
    estado: EstadoAsistencia
    usuario_id: int

class ActualizaAsistencia(SQLModel):
    """
    Esquema para actualizar una asistencia que contiene el fecha, hora_inicio, hora_fin, estado, modulo_id y usuario_id
    """
    fecha: date | None = None
    hora: time | None = None
    estado: EstadoAsistencia | None = None