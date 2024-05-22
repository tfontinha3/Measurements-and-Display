#include <WiFi.h>
#include <WiFiUdp.h>
#include <math.h>

const char* ssid = "xizesse";
const char* password = "sardinhas";

WiFiUDP udp;
const int localUdpPort = 4210; // Local port to listen on
const char *remoteIp = " 10.227.158.39"; // IP address of the receiving host
const int remotePort = 4210; // Port of the receiving host

float velocity = 0.0;
const int bufferSize = 10;
float velocityBuffer[bufferSize];
unsigned long timeBuffer[bufferSize];
int bufferIndex = 0;

void setup() {
    Serial.begin(115200);
    Serial.println("Setuping");
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi connected.");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    udp.begin(localUdpPort);
    Serial.println("UDP server started");
}

void loop() {
    velocity = 100 * sin(2 * PI / 5000 * millis());
    velocityBuffer[bufferIndex] = velocity;
    timeBuffer[bufferIndex] = millis(); 
    bufferIndex = (bufferIndex + 1) % bufferSize;

    sendVelocityData();

    delay(100);
}

void sendVelocityData() {
    char packetBuffer[255]; // Adjust size as needed
    String data = "";

    for (int i = 0; i < bufferSize; i++) {
        data += String(timeBuffer[i]) + "," + String(velocityBuffer[i]) + ";";
    }

    data.toCharArray(packetBuffer, data.length() + 1);
    udp.beginPacket(remoteIp, remotePort);
    udp.write((uint8_t *)packetBuffer, data.length());
    udp.endPacket();
}



