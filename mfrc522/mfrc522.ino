#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN  5 //5
#define RST_PIN 0 //0

extern void publishRegistro(String tagID);
extern void feedbackLectura(bool exito);

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setupRFID() {
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Lector RFID listo.");
}

void leerTarjeta() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  String tagID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagID += String(mfrc522.uid.uidByte[i], HEX);
  }
  tagID.toLowerCase();

  Serial.print("UID detectado: ");
  Serial.println(tagID);

  publishRegistro(tagID);

  feedbackLectura(true);  // ✅ LED verde o azul
  mfrc522.PICC_HaltA();
}