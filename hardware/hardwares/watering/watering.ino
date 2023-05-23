#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

DynamicJsonDocument doc(1024);

const char* ssid = "dlink-7F78";
const char* password = "qwertyuiop";
const char* mqtt_server = "192.168.0.10";
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "13"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

bool activate = false;

const int period = 300000;

const int watering_pin = 5;

const int esp_status_pin = 2;

void setup() {
  Serial.begin(112500);
  pinMode(esp_status_pin, OUTPUT);                        //set pin to input
  digitalWrite(esp_status_pin, HIGH);
  pinMode(watering_pin, OUTPUT);      // set the LED pin mode
  digitalWrite(watering_pin, HIGH);
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
  if (activate) {
    turnOnWatering();
  } else {
    turnOffWatering();
  }
  String response;
  response += F("{\"action\": \"update/watering_status\"");
  response += F(",\"espId\":");
  response += String(MQTT_SERIAL_RECEIVER_CH);
  response += F(",\"activate\":");
  response += String(activate);
  response += F("}");
  publishSerialData(response);
}

void turnOnWatering() {
  digitalWrite(watering_pin, LOW);
  delay(500);
}

void turnOffWatering() {
  digitalWrite(watering_pin, HIGH);
  delay(500);
}

void publishSerialData(String serialData) {
  if (!client.connected()) {
    reconnect();
  }
  int str_len = serialData.length() + 1;

  char char_array[str_len];

  serialData.toCharArray(char_array, str_len);
  client.publish(MQTT_SERIAL_PUBLISH_CH, char_array);
}

void loop() {
  client.loop();
  check_status();
}

void check_status() {
  digitalWrite(esp_status_pin, HIGH);
  delay(500);
  digitalWrite(esp_status_pin, LOW);
  delay(500);
}
