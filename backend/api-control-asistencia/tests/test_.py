def test_healthcheck(client):
    respuesta = client.get("/health")

    assert respuesta.status_code == 200