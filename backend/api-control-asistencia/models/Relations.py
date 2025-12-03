# Importaciones
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

# TYPE_CHECKING es una constante que se utiliza para verificar si se está ejecutando el código en tiempo de ejecución o en tiempo de compilación
if TYPE_CHECKING:
    from .Usuarios import Usuario
    from .Asistencias import Asistencia

# Relaciones
# relationship es una función que se utiliza para establecer una relación entre dos tablas
# Cascade_delete=True y Cascade_update=True son opciones que se utilizan para eliminar o actualizar registros relacionados
# Back_populates es una opción que se utiliza para establecer una relación bidireccional entre dos tablas

# Relacion de Usuario con Asistencias
Usuario.asistencias = relationship(
    "Asistencia", 
    back_populates="usuario",
    cascade_delete=True,
    cascade_update=True
)

# Relacion de Asistencia con Usuario
Asistencia.usuario = relationship(
    "Usuario", 
    back_populates="asistencias",
    cascade_delete=True,
    cascade_update=True
)