#include "secrets.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <MFRC522.h>

// --- IMPORTAR EL MQTT CLIENT USADO EN AWS-IoT.ino ---
extern MQTTClient client;

// --- Referencias de funciones de otros módulos ---
void setupWifi();
void setupAWS();
void leerTarjeta();
void publishRegistro(String tagID);
String getDateTimeString();
void setupTime();
void setupRFID();

// --- Variables globales ---
WiFiClientSecure net;
String currentTag = "";
bool respuestaOK = false;

// --- LED feedback ---
#define LED_OK 2     // LED integrado
#define LED_ERROR 4  // LED externo

// ---------- SETUP PRINCIPAL ----------
void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial.println("Iniciando sistema de control RFID...");

  pinMode(LED_OK, OUTPUT);
  pinMode(LED_ERROR, OUTPUT);

  setupWifi();
  setupTime();
  setupRFID();
  setupAWS();

  Serial.println("Sistema listo para leer tarjetas.");
}

// ---------- LOOP PRINCIPAL ----------
void loop() {

  // Mantener viva la conexión MQTT
  if (!client.connected()) {
    reconnectAWS();
  }
  client.loop(); // recibe mensajes MQTT

  // Leer tarjeta
  leerTarjeta();

  // Latido cada 10 segundos
  static unsigned long lastPing = 0;
  if (millis() - lastPing > 10000) {
    client.publish("asistencia/ping", "{\"status\":\"alive\"}");
    lastPing = millis();
  }

  delay(50);
}

// ---------- FEEDBACK LED ----------
void feedbackLectura(bool exito) {
  if (exito) {
    digitalWrite(LED_OK, HIGH);
    delay(400);
    digitalWrite(LED_OK, LOW);
  } else {
    digitalWrite(LED_ERROR, HIGH);
    delay(600);
    digitalWrite(LED_ERROR, LOW);
  }
}

// ---------- RECONEXIÓN MQTT ----------
void reconnectAWS() {
  Serial.println("⚠️ Conexión perdida. Reintentando...");

  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\n✅ Reconectado a AWS IoT");

  // IMPORTANTE → volver a suscribir
  bool ok = client.subscribe("asistencia/ack");
  Serial.print("Resuscripción a asistencia/ack -> ");
  Serial.println(ok ? "OK" : "FAIL");
}