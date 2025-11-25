#include <WiFiClientSecure.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include "users.h"

extern WiFiClientSecure net;
String getDateTimeString();
MQTTClient client(256);

void setupAWS() {
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
  
  client.begin(AWS_IOT_ENDPOINT, 8883, net);
  client.setKeepAlive(60); // mantiene viva la conexión cada 60 segundos

  Serial.print("Conectando a AWS IoT...");
  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("\n✅ Conectado a AWS IoT");
}

void publishRegistro(String tagID) {
  User* u = getUserFromTag(tagID);
  String datetime = getDateTimeString();

  StaticJsonDocument<512> doc;
  doc["thing"] = THINGNAME;
  doc["tag"] = tagID;
  doc["datetime"] = datetime;
  doc["evento"] = "lectura";  // ← siempre "lectura", el servidor decide el tipo

  if (u) {
    JsonObject user = doc.createNestedObject("user");
    user["id"] = u->id;
    user["nombre"] = u->nombre;
    user["apellido"] = u->apellido;
    user["email"] = u->email;
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