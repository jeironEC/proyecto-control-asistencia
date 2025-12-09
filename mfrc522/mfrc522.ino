#include <SPI.h>
#include <MFRC522.h>
#include <MQTTClient.h>

#define SS_PIN  5
#define RST_PIN 0

extern void publishRegistro(String tagID);
extern MQTTClient client;
extern bool respuestaOK;
extern void feedbackLectura(bool exito);

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setupRFID() {
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Lector RFID listo.");
}

String lastTag = "";

void leerTarjeta() {

  if (!mfrc522.PICC_IsNewCardPresent()) {
    lastTag = "";
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial()) return;

  String tagID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) tagID += "0";
    tagID += String(mfrc522.uid.uidByte[i], HEX);
  }
  tagID.toLowerCase();

  if (tagID == lastTag) {
    mfrc522.PICC_HaltA();
    return;
  }
  lastTag = tagID;

  Serial.print("UID detectado: ");
  Serial.println(tagID);

  // ---------- ENVIAR REGISTRO ----------
  respuestaOK = false;
  publishRegistro(tagID);

  // ---------- ESPERAR OK ----------
  const unsigned long TIMEOUT_MS = 4000;
  unsigned long start = millis();
  bool recibidoOK = false;

  delay(100);   // pequeño margen
  client.loop();

  while (millis() - start < TIMEOUT_MS) {
    client.loop();

    if (respuestaOK) {
      recibidoOK = true;
      break;
    }
    delay(10);
  }

  if (recibidoOK) {
    Serial.println("✅ ACK recibido -> LED azul");
    feedbackLectura(true);
  } else {
    Serial.println("❌ Sin ACK -> LED rojo");
    feedbackLectura(false);
  }

  mfrc522.PICC_HaltA();
}