# Importaciones
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from core.config import CLAVE_SECRETA, ALGORITMO

# ! Agregar comentarios y verificar si se puede tener el tokenUrl aquí
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/inicio_sesion")
contrasena_contexto = CryptContext(schemes=["argon2"], deprecated="auto")

def cifrar_contrasena(contrasena: str):
    """
    Funcion para cifrar la contrasena del usuario.

    Argumentos:
        contrasena (str): Contraseña del usuario

    Devuelve:
        str: Contraseña cifrada
    """
    return contrasena_contexto.hash(contrasena)

def crear_token_acceso(datos: dict, tiempo_expira: timedelta | None = None):
    """
    Funcion para crear un token de acceso, el token expira en 15 minutos por defecto si no se especifica el tiempo de expiracion y se codifica con el algoritmo especificado en la configuracion.

    Argumentos:
        datos (dict): Datos del usuario
        tiempo_expira (timedelta | None): Tiempo de expiracion del token

    Devuelve:
        str: Token de acceso
    """
    codifica = datos.copy()

    if tiempo_expira:
        expira = datetime.now(timezone.utc) + tiempo_expira
    else:
        expira = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    codifica.update({"exp": expira})
    codificacion_jwt = jwt.encode(codifica, CLAVE_SECRETA, algorithm=ALGORITMO)

    return codificacion_jwt