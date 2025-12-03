# Importaciones
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from database.session import engine, obtener_db
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import timedelta
from core.config import CLAVE_SECRETA, ALGORITMO, TIEMPO_EXPIRACION_TOKEN_ACCESO
from core.security import crear_token_acceso, oauth2_scheme
from services.usuario_service import crear_usuario, obtener_usuario_id, obtener_usuario_correo, verificar_contrasena, obtener_usuarios, actualizar_usuario, actualizar_estado_usuario, eliminar_usuario, obtener_rango_asistencias_usuario
from services.asistencia_service import crear_asistencia, obtener_asistencias, obtener_asistencia_id, actualizar_asistencia, eliminar_asistencia
from schemas.usuario import CreaUsuario, ObtenUsuarios, ActualizaUsuario
from schemas.token import Token, TokenData
from schemas.asistencia import CreaAsistencia, ObtenAsistencias, ActualizaAsistencia
from datetime import date

# Evento de inicio: Crea todas las tablas en la base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Evento que se ejecuta al iniciar la aplicación.
    Crea todas las tablas en la base de datos si no existen.
    """
    SQLModel.metadata.create_all(engine)
    yield
    
# Inicialización de la API, agregando titulo y versión
app = FastAPI(
    lifespan=lifespan,
    title="API Control de Asistencia",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(obtener_db)):
    """
    Obtiene el usuario actual a partir del token de autenticación

    Argumentos:
        token (str): Token de autenticación
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Usuario: Usuario actual
    """
    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        id_usuario = datos.get("sub")

        if id_usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
        datos_token = TokenData(id=id_usuario)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
    
    usuario = obtener_usuario_id(datos_token.id, db)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
    return usuario

# PRUEBA DE LA API
@app.get("/health", tags=["Prueba"], summary="Verificar estado de la API")
def health_check(db: Session = Depends(obtener_db)):
    """
    Endpoint de health check para verificar el estado de la API y la conexión a la base de datos.
    
    Retorna:
        dict: Estado de la API y la base de datos
    """
    try:
        # Verificar conexión a la base de datos
        db.exec(select(1))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "ok",
        "database": db_status,
        "version": "1.0.0"
    }

# INICIO DE SESSIÓN
@app.post("/usuarios/inicio_sesion", response_model=Token, tags=["Autenticación"], summary="Iniciar sesión")
def inicio_sesion(datos_formulario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obtener_db)):
    """
    Inicia sesión con las credenciales de un usuario y retorna un token de acceso.
    
    Este endpoint no requiere autenticación previa.

    Argumentos:
        datos_formulario (OAuth2PasswordRequestForm): Credenciales (username=correo, password)
        db (Session): Sesion de la base de datos
    
    Devuelve:
        Token: Token de autenticación JWT y tipo de token
        
    Errores:
        - 400: Usuario no encontrado, contraseña incorrecta o usuario inactivo
        
    Ejemplo:
        username: usuario@ejemplo.com
        password: micontraseña123
    """
    # Primero verificar si el usuario existe
    usuario = obtener_usuario_correo(datos_formulario.username, db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario o contraseña incorrectos")
    
    # Verificar si el usuario está activo
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no esta activado")
    
    # Verificar la contraseña
    if not verificar_contrasena(datos_formulario.password, usuario.contrasena):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario o contraseña incorrectos")

    token_acceso = crear_token_acceso({"sub": usuario.id}, timedelta(minutes=int(TIEMPO_EXPIRACION_TOKEN_ACCESO)))
    return {"access_token": token_acceso, "token_type": "bearer"}
    
# CRUD USUARIOS
@app.post("/usuario", response_model=dict, tags=["Usuarios"], summary="Crear un nuevo usuario", status_code=status.HTTP_201_CREATED)
def crea_usuario(usuario: CreaUsuario, db: Session = Depends(obtener_db)):
    """
    Crea un nuevo usuario en el sistema.
    
    Este endpoint no requiere autenticación ya que es usado para el registro de nuevos usuarios.

    Argumentos:
        usuario (CreaUsuario): Datos del usuario a crear (nombre, correo, contraseña, etc.)
        db (Session): Sesion de la base de datos
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 400: El correo ya está registrado
        - 500: Error al crear el usuario
    """
    if obtener_usuario_correo(usuario.correo, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya esta registrado")
    
    resultado = crear_usuario(usuario, db)

    if resultado:
        return {"msg": "Usuario creado correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar crear el usuario")

@app.get("/usuarios", response_model=list[ObtenUsuarios], tags=["Usuarios"], summary="Obtener todos los usuarios")
def usuarios(db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Obtiene la lista completa de todos los usuarios registrados.
    
    Requiere autenticación.

    Argumentos:
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        list[ObtenUsuarios]: Lista de usuarios
        
    Errores:
        - 401: No autenticado o token inválido
        - 500: Error al obtener los usuarios
    """
    resultados = obtener_usuarios(db)

    if not resultados:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar obtener todos los usuarios")
    return resultados

@app.get("/usuario/{id}", response_model=ObtenUsuarios, tags=["Usuarios"], summary="Obtener usuario por ID")
def usuario_id(id: int, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Obtiene la información de un usuario específico por su ID.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID del usuario a buscar
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        ObtenUsuarios: Datos del usuario encontrado
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Usuario no encontrado
    """
    usuario = obtener_usuario_id(id, db)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return ObtenUsuarios.model_validate(usuario)

@app.patch("/usuario/{id}", response_model=dict, tags=["Usuarios"], summary="Actualizar usuario")
def actualiza_usuario(id: int, datos: ActualizaUsuario, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Actualiza los datos de un usuario existente.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID del usuario a actualizar
        datos (ActualizaUsuario): Datos a actualizar (nombre, correo, etc.)
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Usuario no encontrado
        - 500: Error al actualizar el usuario
    """
    usuario = actualizar_usuario(id, datos, db)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    if usuario:
        return {"msg": "Usuario actualizado correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar actualizar el usuario") 

@app.patch("/usuario/estado/{id}", response_model=dict, tags=["Usuarios"], summary="Activar/desactivar usuario")
def actualiza_estado_usuario(id: int, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Alterna el estado activo/inactivo de un usuario.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID del usuario
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Usuario no encontrado
        - 500: Error al actualizar el estado
    """
    estado_usuario = actualizar_estado_usuario(id, db)

    if estado_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    if estado_usuario:
        return {"msg": "Estado de usuario actualizado correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar actualizar el usuario") 

@app.delete("/usuario/{id}", response_model=dict, tags=["Usuarios"], summary="Eliminar usuario", status_code=status.HTTP_200_OK)
def elimina_usuario(id: int, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Elimina un usuario del sistema.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID del usuario a eliminar
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Usuario no encontrado
        - 500: Error al eliminar el usuario
    """
    usuario = eliminar_usuario(id, db)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    if usuario:
        return {"msg": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar eliminar el usuario") 

# ASISTENCIAS
@app.post("/asistencia", response_model=dict, tags=["Asistencias"], summary="Crear una nueva asistencia", status_code=status.HTTP_201_CREATED)
def crea_asistencia(asistencia: CreaAsistencia, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Registra una nueva asistencia de un usuario a un módulo.
    
    Requiere autenticación.

    Argumentos:
        asistencia (CreaAsistencia): Datos de la asistencia (fecha, hora, estado, usuario_id)
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 500: Error al crear la asistencia
    """
    resultado = crear_asistencia(asistencia, db)

    if resultado:
        return {"msg": "Asistencia creada correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar crear la asistencia")

@app.get("/asistencias", response_model=list[ObtenAsistencias], tags=["Asistencias"], summary="Obtener todas las asistencias")
def asistencias(db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Obtiene la lista completa de todas las asistencias registradas.
    
    Requiere autenticación.

    Argumentos:
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        list[ObtenAsistencias]: Lista de asistencias
        
    Errores:
        - 401: No autenticado o token inválido
        - 500: Error al obtener las asistencias
    """
    resultados = obtener_asistencias(db)

    if not resultados:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar obtener todas las asistencias")
    return resultados

@app.get("/asistencia/{id}", response_model=ObtenAsistencias, tags=["Asistencias"], summary="Obtener asistencia por ID")
def asistencia_id(id: int, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Obtiene la información de una asistencia específica por su ID.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID de la asistencia a buscar
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        ObtenAsistencias: Datos de la asistencia encontrada
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Asistencia no encontrada
    """
    asistencia = obtener_asistencia_id(id, db)
    if asistencia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
    return ObtenAsistencias.model_validate(asistencia)

@app.get("/usuario/asistencias/{id}/{fecha_inicial}/{fecha_final}", response_model=list[ObtenAsistencias], tags=["Asistencias"], summary="Buscar asistencias por rango de fechas")
def usuario_asistencias(id: int, fecha_inicial: date, fecha_final: date, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):    
    """
    Obtiene las asistencias de un usuario específico filtradas por un rango de fechas.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID del usuario
        fecha_inicial (date): Fecha de inicio del rango (formato: YYYY-MM-DD)
        fecha_final (date): Fecha de fin del rango (formato: YYYY-MM-DD)
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        list[ObtenAsistencias]: Lista de asistencias en el rango especificado
        
    Errores:
        - 400: Rango de fechas inválido (fecha_inicial > fecha_final)
        - 401: No autenticado o token inválido
        
    Ejemplo:
        GET /usuario/asistencias/1/2024-01-01/2024-01-31
    """
    # Validar que el rango de fechas sea válido
    if fecha_inicial > fecha_final:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La fecha inicial no puede ser mayor que la fecha final"
        )
    
    asistencias = obtener_rango_asistencias_usuario(id, fecha_inicial, fecha_final, db)

    return asistencias

@app.patch("/asistencia/{id}", response_model=dict, tags=["Asistencias"], summary="Actualizar asistencia")
def actualiza_asistencia(id: int, datos: ActualizaAsistencia, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Actualiza los datos de una asistencia existente.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID de la asistencia a actualizar
        datos (ActualizaAsistencia): Datos a actualizar
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Asistencia no encontrada
        - 500: Error al actualizar la asistencia
    """
    asistencia = actualizar_asistencia(id, datos, db)

    if asistencia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
    
    if asistencia:
        return {"msg": "Asistencia actualizada correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar actualizar la asistencia")

@app.delete("/asistencia/{id}", response_model=dict, tags=["Asistencias"], summary="Eliminar asistencia", status_code=status.HTTP_200_OK)
def elimina_asistencia(id: int, db: Session = Depends(obtener_db), usuario_actual = Depends(obtener_usuario_actual)):
    """
    Elimina una asistencia del sistema.
    
    Requiere autenticación.

    Argumentos:
        id (int): ID de la asistencia a eliminar
        db (Session): Sesion de la base de datos
        usuario_actual: Usuario autenticado
    
    Devuelve:
        dict: Mensaje de confirmación
        
    Errores:
        - 401: No autenticado o token inválido
        - 404: Asistencia no encontrada
        - 500: Error al eliminar la asistencia
    """
    asistencia = eliminar_asistencia(id, db)

    if asistencia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
    
    if asistencia:
        return {"msg": "Asistencia eliminada correctamente"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrio un error al intentar eliminar la asistencia")