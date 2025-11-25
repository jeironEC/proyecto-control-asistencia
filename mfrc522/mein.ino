#include "secrets.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <MFRC522.h>

// --- Referencias de funciones de otros módulos ---
void setupWifi();
void setupAWS();
void reconnectAWS();
void leerTarjeta();
void publishRegistro(String tagID);
String getDateTimeString();
void setupTime();
void setupRFID();

// --- Variables globales ---
WiFiClientSecure net;
String currentTag = "";

// --- LED feedback ---
#define LED_OK 2     // LED integrado en muchas ESP32
#define LED_ERROR 4  // si tienes un LED externo opcional

// --- Setup principal ---
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

// --- Loop principal ---
void loop() {
  // Mantener viva la conexión MQTT
  if (!client.connected()) {
    reconnectAWS(); // tu función de reconexión
  }
  client.loop(); // 🔹 Mantiene el ping y recibe mensajes

  // Leer tarjeta si está presente
  leerTarjeta();

  // --- Latido cada 10 segundos ---
  static unsigned long lastPing = 0;
  if (millis() - lastPing > 10000) { // cada 10 s
    client.publish("asistencia/ping", "{\"status\":\"alive\"}");
    lastPing = millis();
  }

  delay(100); // pequeño delay, pero no más de 200 ms
}

// --- Función para feedback visual ---
void feedbackLectura(bool exito) {
  if (exito) {
    digitalWrite(LED_OK, HIGH);
    delay(200);
    digitalWrite(LED_OK, LOW);
  } else {
    digitalWrite(LED_ERROR, HIGH);
    delay(500);
    digitalWrite(LED_ERROR, LOW);
  }
}

void reconnectAWS() {
  while (!client.connect(THINGNAME)) {
    Serial.print("Reconectando a AWS IoT...");
    delay(1000);
  }
  Serial.println("✅ Reconectado a AWS IoT");
}