#include <Wire.h>
#include <Adafruit_BMP085.h>
#include "heltec.h"

#define SOIL_SENSOR 36
#define BAND 915E6
#define TRANSMIT_INTERVAL 1500

Adafruit_BMP085 bmp;

void setup() {
  Heltec.begin(true, true, false); // Display, LoRa, Serial
  
  Wire.begin(4, 15); // I2C pins for Heltec V2
  
  if (!bmp.begin()) {
    displayCenteredMessage("BMP180 FAIL", ArialMT_Plain_16);
    while(1);
  }

  // LoRa configuration
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.setPreambleLength(8);
  LoRa.setSyncWord(0x12);
  
  // OLED setup
  Heltec.display->flipScreenVertically();
  Heltec.display->setContrast(255);
  displayCenteredMessage("Transmitting...", ArialMT_Plain_10);
}

void loop() {
  float temp = bmp.readTemperature();
  float pres = bmp.readPressure()/100.0;
  int moist = analogRead(SOIL_SENSOR);
  
  updateDisplay(temp, pres, moist);
  
  // Send via LoRa (comma-separated)
  LoRa.beginPacket();
  LoRa.print(temp, 1);
  LoRa.print(",");
  LoRa.print(pres, 1);
  LoRa.print(",");
  LoRa.print(moist);
  LoRa.endPacket();
  
  delay(TRANSMIT_INTERVAL);
}

void updateDisplay(float temp, float pres, int moist) {
  Heltec.display->clear();
  
  // Temperature
  Heltec.display->setFont(ArialMT_Plain_16);
  Heltec.display->drawString(0, 0, "Temp:");
  Heltec.display->setFont(ArialMT_Plain_24);
  Heltec.display->drawString(0, 16, String(temp,1) + "°C");
  
  // Pressure
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 42, "Pres: " + String(pres,1) + " hPa");
  
  // Moisture
  Heltec.display->drawString(0, 52, "Mois: " + String(moist));
  
  Heltec.display->display();
}

void displayCenteredMessage(String msg, const uint8_t* font) {
  Heltec.display->clear();
  Heltec.display->setFont(font);
  int16_t x = (128 - Heltec.display->getStringWidth(msg)) / 2;
  int16_t y = (64 - getFontHeight(font)) / 2;
  Heltec.display->drawString(x, y, msg);
  Heltec.display->display();
}

// Helper function to get font height
int getFontHeight(const uint8_t* font) {
  if (font == ArialMT_Plain_10) return 10;
  if (font == ArialMT_Plain_16) return 16;
  if (font == ArialMT_Plain_24) return 24;
  return 10; // default
}