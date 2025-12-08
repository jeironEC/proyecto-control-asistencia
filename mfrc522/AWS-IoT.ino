#include <WiFiClientSecure.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include "users.h"

extern WiFiClientSecure net;
String getDateTimeString();
MQTTClient client(256);
extern bool respuestaOK;
extern void feedbackLectura(bool exito);

// --- CALLBACK PRINCIPAL MQTT ---
void onMessageCallback(String &topic, String &payload) {
  Serial.println("=== MQTT MESSAGE RECEIVED ===");
  Serial.print("TOPIC: ");
  Serial.println(topic);
  Serial.print("PAYLOAD: ");
  Serial.println(payload);

  payload.trim();

  if (topic.equals("asistencia/ack")) {
    if (payload.equalsIgnoreCase("OK")) {
      respuestaOK = true;
      Serial.println("-> Recibido ACK = OK");
    } else {
      respuestaOK = false;
      Serial.println("-> Payload recibido NO es OK");
    }
  }
}

void setupAWS() {
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);

  client.begin(AWS_IOT_ENDPOINT, 8883, net);
  client.onMessage(onMessageCallback);
  client.setKeepAlive(60);

  Serial.print("Conectando a AWS IoT...");
  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("\n✅ Conectado a AWS IoT");

  // -------------------------
  // SUSCRIPCIÓN AL ACK
  // -------------------------
  bool ok = client.subscribe("asistencia/ack");
  Serial.print("Suscripción a asistencia/ack -> ");
  Serial.println(ok ? "OK" : "FAIL");
}

void publishRegistro(String tagID) {
  User* u = getUserFromTag(tagID);
  String datetime = getDateTimeString();

  StaticJsonDocument<512> doc;
  doc["thing"] = THINGNAME;
  doc["tag"] = tagID;
  doc["datetime"] = datetime;
  doc["evento"] = "lectura";

  if (u) {
    JsonObject user = doc.createNestedObject("user");
    user["id"] = u->id;
    user["nombre"] = u->nombre;
    user["apellido"] = u->apellido;
    user["email"] = u->email;
    user["rol"] = u->rol;
  }

  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);

  Serial.println("📤 Enviando a AWS IoT:");
  Serial.println(jsonBuffer);

  if (client.connected()) {
    client.publish("asistencia/registro", jsonBuffer);
  } else {
    Serial.println("⚠️ No conectado a AWS IoT.");
  }
}