import datetime
from schemas.asistencia import CreaAsistencia, EstadoAsistencia
from datetime import date


def test_crea_asistencia(client, usuario):
    print("HOLA:", usuario)
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')

    datos = CreaAsistencia(
        fecha=fecha_actual,
        hora=hora_actual,
        estado= EstadoAsistencia.PRESENTE,
        usuario_id=usuario["id"]
    )

    respuesta = client.post("/asistencia", json=datos.model_dump(mode="json"))

    assert respuesta.status_code == 201

    respuesta_json = respuesta.json()

    assert "id" in respuesta_json
    assert "fecha" in respuesta_json
    assert "hora" in respuesta_json
    assert "estado" in respuesta_json
    assert "usuario_id" in respuesta_json

    assert respuesta_json["id"] == 1
    assert respuesta_json["fecha"] == fecha_actual
    assert respuesta_json["hora"] == hora_actual
    assert respuesta_json["estado"] == "presente"
    assert respuesta_json["usuario_id"] == usuario["id"]
