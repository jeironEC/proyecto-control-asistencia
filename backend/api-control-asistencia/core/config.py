# Importaciones
import os
import secrets
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables constantes con valores obtenidos de variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL") # URL de conexión con la base de datos
CLAVE_SECRETA = secrets.token_hex(32) # Clave secreta para hashear contraseña de los usuarios
ALGORITMO = os.getenv("ALGORITHM") # Algoritmo utilizado para hashear la contraseña
TIEMPO_EXPIRACION_TOKEN_ACCESO = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") # Tiempo de validez del token generado para la contraseña