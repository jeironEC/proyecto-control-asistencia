from schemas.usuario import CreaUsuario
from models.Usuarios import RolUsuario

def test_creacion_usuario(client):
    datos = CreaUsuario(
        nombre="Jeiron",
        apellido="Espinal",
        correo="jeiron.espinal@gmail.com",
        contrasena="Jeiron123",
        rol=RolUsuario.ALUMNO,
        activo=1,
    )

    respuesta = client.post("/usuario", json=datos.model_dump(mode="json"))

    assert respuesta.status_code == 201

    respuesta_json = respuesta.json()

    assert "id" in respuesta_json
    assert "nombre" in respuesta_json
    assert "apellido" in respuesta_json
    assert "correo" in respuesta_json
    assert "rol" in respuesta_json
    assert "activo" in respuesta_json

    assert respuesta_json["nombre"] == "Jeiron"
    assert respuesta_json["apellido"] == "Espinal"
    assert respuesta_json["correo"] == "jeiron.espinal@gmail.com"
    assert respuesta_json["rol"] == "alumno"
    assert respuesta_json["activo"] == True