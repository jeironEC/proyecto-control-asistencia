# Importaciones
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, ForeignKey
from enum import Enum
from datetime import date, time

class EstadoAsistencia(Enum):
    """
    Enum para los estados de la asistencia que puede ser PRESENTE, AUSENTE, RETRASO o JUSTIFICADA

    Argumentos:
        PRESENTE (str): Estado de la asistencia
        AUSENTE (str): Estado de la asistencia
        RETRASO (str): Estado de la asistencia
        JUSTIFICADA (str): Estado de la asistencia

    Devuelve:
        EstadoAsistencia: Enum con los estados de la asistencia
    """
    PRESENTE = "presente"
    AUSENTE = "ausente"
    RETRASO = "retraso"
    JUSTIFICADA = "justificada"

class Asistencia(SQLModel, table=True):
    """
    Modelo para las asistencias que contiene los siguientes campos:

    Campos:
        id (int): Id de la asistencia
        fecha (date): Fecha de la asistencia
        hora (time): Hora de la asistencia
        estado (EstadoAsistencia): Estado de la asistencia
        usuario_id (int): Id del usuario que pertenece la asistencia
    """
    __tablename__ = "asistencia"
    
    id: int = Field(primary_key=True)
    fecha: date
    hora: time
    estado: EstadoAsistencia

    usuario_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("usuario.id", ondelete="CASCADE")
        )
    )