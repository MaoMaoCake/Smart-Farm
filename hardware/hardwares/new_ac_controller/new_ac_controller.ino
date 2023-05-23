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
#define MQTT_SERIAL_RECEIVER_CH "5"

const int on_off_pin = 12;
const int temp_up_pin = 13;
const int temp_down_pin = 14;
const int esp_status_pin = 2;

WiFiClient wifiClient;

PubSubClient client(wifiClient);

boolean current_ac_status = false;
boolean new_ac_status = false;
int current_temperature = 0;
int new_temperature = 0;
boolean on_init = false;

void setup() {
  Serial.begin(115200);

  pinMode(on_off_pin, OUTPUT);      // set the LED pin mode
  pinMode(temp_up_pin, OUTPUT);
  pinMode(temp_down_pin, OUTPUT);
  pinMode(esp_status_pin, OUTPUT);
  digitalWrite(on_off_pin, HIGH);
  digitalWrite(temp_up_pin, HIGH);
  digitalWrite(temp_down_pin, HIGH);
  digitalWrite(esp_status_pin, HIGH);

  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
  getAcStatus();
  Serial.print("Temperature:");
  Serial.println(current_temperature);
  Serial.print("AC status:");
  Serial.println(current_ac_status);
}

void setup_wifi() {
  delay(10);
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
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected");
      client.publish("/icircuit/presence/ESP32/", "hello world");
      client.subscribe(MQTT_SERIAL_RECEIVER_CH);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
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
  if (!on_init) {
    current_temperature = doc["temperature"];
    current_ac_status = doc["ac_status"];
    on_init = true;
    return;
  }
  if (doc["temperature"]) {
    new_temperature = doc["temperature"];
    Serial.print("new_temperature: ");
    Serial.println(new_temperature);
  }
  if (doc["activate"] || !doc["activate"]) {
    Serial.print("new_ac_status: ");
    new_ac_status = doc["activate"];
    Serial.println(new_ac_status);
  }

  Serial.print("current_temperature: ");
  Serial.println(current_temperature);
  Serial.print("current_ac_status: ");
  Serial.println(current_ac_status);
  if ((new_temperature != current_temperature) || (new_ac_status != current_ac_status)) {
    acCommand();
  }
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

void getAcStatus() {
  String getAcStatusRequest = "{\"action\":\"get/ac_status\",\"espId\":";
  getAcStatusRequest += String(MQTT_SERIAL_RECEIVER_CH);
  getAcStatusRequest += F("}");
  publishSerialData(getAcStatusRequest);
}

void acCommand() {
  if (new_ac_status != current_ac_status) {
    turnOnOffAc();
  }
  int iteration = new_temperature - current_temperature;
  for (int i = 0; i < abs(iteration); i++) {
    if (iteration < 0) {
      tempDown();
    } else if (iteration > 0) {
      tempUp();
    } else {
      continue;
    }
  }
  current_ac_status = new_ac_status;
  current_temperature = new_temperature;
  sendAcStatus();
}

void sendAcStatus() {
  String response;
  response += F("{\"action\": \"update/ac_status\"");
  response += F(",\"espId\":");
  response += String(MQTT_SERIAL_RECEIVER_CH);
  response += F(",\"temperature\":");
  response += String(current_temperature);
  response += F(",\"ac_status\":");
  response += String(current_ac_status);
  response += F("}");

  publishSerialData(response);
}

void turnOnOffAc() {
  digitalWrite(on_off_pin, LOW);
  delay(500);
  digitalWrite(on_off_pin, HIGH);
  delay(500);
  Serial.println("turn on/off ac");
}

void tempUp() {
  digitalWrite(temp_up_pin, LOW);
  delay(500);
  digitalWrite(temp_up_pin, HIGH);
  delay(500);
  digitalWrite(temp_up_pin, LOW);
  delay(500);
  digitalWrite(temp_up_pin, HIGH);
  delay(500);
  Serial.println("temp up ac");
}

void tempDown() {
  digitalWrite(temp_down_pin, LOW);
  delay(500);
  digitalWrite(temp_down_pin, HIGH);
  delay(500);
  digitalWrite(temp_down_pin, LOW);
  delay(500);
  digitalWrite(temp_down_pin, HIGH);
  delay(500);
  Serial.println("temp down ac");
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
