#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <IRremote.h>

DynamicJsonDocument doc(1024);

// Update these with values suitable for your network.
const char* ssid = "PD_LAPTOP";
const char* password = "012345679";
const char* mqtt_server = "192.168.137.1";
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "5"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

const int ir_pin = 19;
IRsend irsend(ir_pin);

bool current_ac_status = false;
bool new_ac_status = false;
int current_temperature = 0;
int new_temperature = 0;
bool on_init = false;

void setup() {
  Serial.begin(115200);

  pinMode(12, OUTPUT);      // set the LED pin mode
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
  if(!on_init){
    current_temperature = doc["temperature"];
    current_ac_status = doc["activate"];
    on_init = true;
  }
  if(doc["temperature"]){
    new_temperature = doc["temperature"];
  }
  if(doc["activate"]){
    new_ac_status = doc["activate"];
  }
  if((new_temperature != current_temperature) || (new_ac_status != current_ac_status)){
    acCommand();
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

void getAcStatus(){
  String getAcStatusRequest = "{\"action\":\"get/ac_status\",\"espId\":";
  getAcStatusRequest += String(MQTT_SERIAL_RECEIVER_CH);
  getAcStatusRequest += F("}");
  publishSerialData(getAcStatusRequest);
}

void acCommand(){
  if(new_ac_status != current_ac_status){
    if(new_ac_status){
      openAc();
    } else {
      closeAc();
    }
  }
  int iteration = new_temperature - current_temperature;
  for (int i = 0; i < abs(iteration); i++) {
    if(iteration < 0){
      tempDown();
    } else if (iteration > 0){
      tempUp();
    } else {
      continue;
    }
  }
  current_ac_status = new_ac_status;
  current_temperature = new_temperature;
  sendAcStatus();
}

void sendAcStatus(){
  String response;
  response += F("{\"action\": \"update/ac_status\"");
  response += F(",\"espId\":");
  response += String(MQTT_SERIAL_RECEIVER_CH);
  response += F(",\"temperature\":");
  response += String(current_temperature);
  response += F(",\"ac_status\":");
  response += String(current_ac_status);
  response += F("}");

  Serial.println(response);
}

void openAc(){
  
}

void closeAc(){
  
}

void tempUp(){
  
}

void tempDown(){
  
}

void loop() {
  client.loop();
}
