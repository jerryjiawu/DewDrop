#include <heltec.h>

#define BAND 915E6

void setup() {
  Heltec.begin(true, true, true); // Display, LoRa, Serial
  Serial.begin(115200);
  
  // LoRa config (must match transmitter)
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.setPreambleLength(8);
  LoRa.setSyncWord(0x12);
  
  // Display setup
  Heltec.display->flipScreenVertically();
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 0, "LoRa Receiver Ready");
  Heltec.display->display();
  
  Serial.println("millis,temp,pres,moist,rssi,snr");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String received = "";
    
    while (LoRa.available()) {
      received += (char)LoRa.read();
    }
    
    int rssi = LoRa.packetRssi();
    float snr = LoRa.packetSnr();
    
    updateDisplay(received, rssi, snr);
    
    // Print CSV to Serial
    Serial.print(millis());
    Serial.print(",");
    Serial.print(received);
    Serial.print(",");
    Serial.print(rssi);
    Serial.print(",");
    Serial.println(snr);
  }
  delay(10);
}

void updateDisplay(String data, int rssi, float snr) {
  Heltec.display->clear();
  
  // Signal info
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 0, "RSSI:" + String(rssi));
  Heltec.display->drawString(64, 0, "SNR:" + String(snr,1));
  
  // Received data
  Heltec.display->drawString(0, 12, data);
  
  Heltec.display->display();
}