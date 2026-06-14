/**
 * @file air_quality_node.ino
 * @brief IoT Air Quality & Pollution Monitoring Node for ESP32
 */

#include <WiFi.h>
#include "ThingSpeak.h"
#include "DHT.h"

#define DHTPIN 4          
#define DHTTYPE DHT22     
#define MQ135_PIN 34      
#define BUZZER_PIN 25     
#define LED_GREEN 18      
#define LED_RED 19        

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
unsigned long CLOUD_CHANNEL_ID = 2222222;         
const char* CLOUD_WRITE_API_KEY = "YOUR_API_KEY"; 

DHT dht(DHTPIN, DHTTYPE);
WiFiClient networkClient;

const int CLEAN_AIR_THRESHOLD = 800;   
const int MODERATE_AIR_THRESHOLD = 1800; 
const int TOXIC_AIR_THRESHOLD = 3000;    

unsigned long lastUploadTimestamp = 0;
const unsigned long UPLOAD_INTERVAL_MS = 20000; 

void setup() {
  Serial.begin(115200);
  pinMode(MQ135_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  dht.begin();
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  ThingSpeak.begin(networkClient);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  int gas = analogRead(MQ135_PIN);

  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  int severity = 0;
  if (gas <= CLEAN_AIR_THRESHOLD) {
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, LOW);
    noTone(BUZZER_PIN);
  } else if (gas <= MODERATE_AIR_THRESHOLD) {
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, HIGH);
    noTone(BUZZER_PIN);
  } else {
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);
    tone(BUZZER_PIN, 1000);
    severity = 2;
  }

  Serial.printf("Temp: %.1f C, Hum: %.1f%%, Gas: %d\n", t, h, gas);

  if (millis() - lastUploadTimestamp >= UPLOAD_INTERVAL_MS) {
    ThingSpeak.setField(1, gas);
    ThingSpeak.setField(2, t);
    ThingSpeak.setField(3, h);
    ThingSpeak.setField(4, severity);
    ThingSpeak.writeFields(CLOUD_CHANNEL_ID, CLOUD_WRITE_API_KEY);
    lastUploadTimestamp = millis();
  }
  delay(2000);
}
