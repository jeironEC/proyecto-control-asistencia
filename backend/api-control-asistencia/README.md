# api control asistencia

## Descripción
Esta API es un proyecto creado para utilizarse con fines educativos...

### Requerimientos
* Lenguaje:
    - python ~3.12

* Framework:
    - FastAPI

* Librerias adicionales para el funcionamiento:
    - uvicorn
    - sqlmodel
    - pymysql
    - python-dotenv
    - pyjwt[crypto]
    - passlib[bcrypt]
    - pwdlib[argon2]

### Entorno virtual
Se recomiendo utilizar un entorno virtual para la ejecución de la API.
Creación de un entorno virtual:
    - python3.12 -m .venv venv (donde .venv es el nombre de la carpeta del entorno) (la versión de python puede ser cualquiera posterior a 3.12)

Activación del entorno:
    * En linux:
        - source .venv/bin/activate

Desactivación del entorno:
    * En linux:
        - deactivate

### Instalación de los requerimientos
Para poder iniciar el servidor de la api es necesario instalar los requerimientos en el entorno virtual
Instalación de los requerimientos:
    - pip install -r requirements.txt

### Variables de entorno
Se necesita una variable de entorno para la url de conexion con la base de datos.
Se debe crear el archivo .env y agregar la siguiente variable de entorno:
    - DATABASE_URL="mysql+pymysql://usuario:contrasena@nombre_host:puerto/nombre_db"

    Explicación:
        - mysql: indica el tipo de base de datos.
        - pymysql: es el driver de python, que usa como medio para conectarse con la base de datos.
        - usuario: es el usuario del sistema de gestion de base de datos.
        - contrasena: es la contraseña del sistema de gestion de base de datos.
        - nombre_host: es la ip o hostname donde se encuentra la base de datos.
        - puerto: es el puerto de MySQL.
        - nombre_db: es el nombre de la base de datos en el sistema de gestion de base de datos.