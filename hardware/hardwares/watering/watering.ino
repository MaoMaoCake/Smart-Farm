#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

DynamicJsonDocument doc(1024);

// Update these with values suitable for your network.
const char* ssid = "PD_LAPTOP";
const char* password = "012345679";
const char* mqtt_server = "192.168.137.250";
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "13"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

bool activate = false;

const int watering_pin = 2;

void setup() {
  Serial.begin(112500);

  pinMode(watering_pin, OUTPUT);      // set the LED pin mode
  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected");
      //Once connected, publish an announcement...
      client.publish("/icircuit/presence/ESP32/", "hello world");
      // ... and resubscribe
      client.subscribe(MQTT_SERIAL_RECEIVER_CH);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
  Serial.println("-------new message from broker-----");
  Serial.print("channel:");
  Serial.println(topic);
  Serial.print("data:");
  Serial.write(payload, length);
  Serial.println();
  DeserializationError error = deserializeJson(doc, payload);
  if (error)
    return;
  activate = doc["activate"];
  if(activate){
    turnOnWatering();
  } else {
    turnOffWatering();
  }
}

void turnOnWatering(){
  digitalWrite(watering_pin,LOW);
//  String updateData;
//  updateData += F("{\"action\": \"update/dehumidifier\"");
//  updateData += F(",\"activate\":");
//  updateData += String(activate);
//  updateData += F("}");
//  publishSerialData(updateData);
}

void turnOffWatering(){
  digitalWrite(watering_pin,HIGH);
//  String updateData;
//  updateData += F("{\"action\": \"update/dehumidifier\"");
//  updateData += F(",\"activate\":");
//  updateData += String(activate);
//  updateData += F("}");
//  publishSerialData(updateData);
}

void publishSerialData(String serialData) {
  if (!client.connected()) {
    reconnect();
  }
  int str_len = serialData.length() + 1; 
  
  // Prepare the character array (the buffer) 
  char char_array[str_len];
  
  // Copy it over 
  serialData.toCharArray(char_array, str_len);
  client.publish(MQTT_SERIAL_PUBLISH_CH, char_array);
}

void loop() {
  client.loop();
}
