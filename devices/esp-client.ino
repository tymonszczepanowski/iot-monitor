/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <WiFi.h>
#

const char* ssid     = "AndroidAP_9192";
const char* password = "12345678";

const char* host = "192.168.43.215";
const char* streamId   = "....................";
const char* privateKey = "....................";

void setup()
{
    Serial.begin(115200);
    delay(10);

    pinMode(34, OUTPUT);
    pinMode(35, INPUT);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

int value = 0;

void loop()
{
    delay(5000);
    

    Serial.print("connecting to ");
    Serial.println(host);

    // Use WiFiClient class to create TCP connections
    WiFiClient client;
    const int httpPort = 20000;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }

    while(true){
      int dst = getSensorDistance();
      Serial.println(dst);
      client.print(dst);
      delay(2000);
    }
}

int getSensorDistance(){

  digitalWrite(34, LOW);
  delayMicroseconds(2);

  digitalWrite(34, HIGH);
  delayMicroseconds(10);
  digitalWrite(34, LOW);

  long duration = pulseIn(35, HIGH);

  int distance = duration * 0.034 / 2;

  return distance;
  
}
