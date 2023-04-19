#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <ArduinoJson.h>


DynamicJsonDocument doc(1024);


#define DHTPIN 5          // Pin to which DHT11 sensor is connected
#define DHTTYPE DHT11     // DHT11 sensor type


DHT dht(DHTPIN, DHTTYPE); // Create DHT object

int count = 0;
int send_time_interval = 10;

// Update these with values suitable for your network.
const char* ssid = "PD_LAPTOP";
const char* password = "012345679";
const char* mqtt_server = "192.168.137.250";
int maxHumidity = 0;
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "3"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

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
  maxHumidity = doc["humidity"];
}

void setup() {
  Serial.begin(115200);

  Serial.print("MG-811 Demostration\n"); 
  dht.begin();           // Initialize DHT sensor
  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
  setThreshold();
  Serial.print("Max Humidity\n"); 
  Serial.println(maxHumidity);
  
}

void setThreshold(){
  String thresholdRequest = "{\"action\":\"get/threshold\",\"espId\":";
  thresholdRequest += String(MQTT_SERIAL_RECEIVER_CH);
  thresholdRequest += F("}");
  publishSerialData(thresholdRequest);
}

void turnOnDehumidifier(){
  String dehumidifierRequest = F("{\"action\": \"turn_on/dehumidifier\"}");
  publishSerialData(dehumidifierRequest);
}

void turnOffDehumidifier(){
  String dehumidifierRequest = F("{\"action\": \"turn_off/dehumidifier\"}");
  publishSerialData(dehumidifierRequest);
}

String collectAllSensorData() {
  
  float humidity = dht.readHumidity();    // Read humidity value from sensor
  float temperature = dht.readTemperature();  // Read temperature value from sensor
  
  // Check if any reading failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    // Print temperature and humidity values
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C  |  ");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  if (maxHumidity > 0){
    if (int(humidity) > maxHumidity){
      Serial.print("Humidity is over limit");
      turnOnDehumidifier();
      Serial.println(maxHumidity);
    } else {
      turnOffDehumidifier();
    }
  }
    
  String response;
  response += F("{\"action\": \"update/sensors\"");
  response += F(",\"espId\":");
  response += String(MQTT_SERIAL_RECEIVER_CH);
  response += F(",\"temperature\":");
  response += String(temperature, 6);
  response += F(",\"humidity\":");
  response += String(humidity, 6);
  response += F("}");

  Serial.println(response);
  
  return response;
  }
    
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
  String message = collectAllSensorData();
  Serial.println("-------new message from broker-----");
  if (count == send_time_interval){
    publishSerialData(message);
    count = 0;
  }
  Serial.println(count);
  delay(1000);
  count += 1;
}
