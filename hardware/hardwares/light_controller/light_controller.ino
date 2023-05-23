#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

DynamicJsonDocument doc(1024);

// Update these with values suitable for your network.
const char* ssid = "dlink-7F78";
const char* password = "qwertyuiop";
const char* mqtt_server = "192.168.0.10";
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "7"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

const int esp_status_pin = 2;

float T = 0.115;
int UVPin = 23;
int IRPin = 5;
int NLPin = 4;
Servo UVs;
Servo IRs;
Servo NLs;

int currentUV = 0;
int currentIR = 0;
int currentNL = 0;

bool currentState = 1;

int testPin = 21;

//modify angle here, not 30 degree but around 45 degree is better i guess
////for id = 8
////left maybe 220-250
//int lUVangle = 200;
//int lIRangle = 220;
//int lNLangle = 220;
////right maybe 150-200
//int rUVangle = 160;
//int rIRangle = 160;
//int rNLangle = 150;

//for id = 7
//left maybe 220-250
int lUVangle = 250;
int lIRangle = 230;
int lNLangle = 225;
//right maybe 150-200
int rUVangle = 180;
int rIRangle = 160;
int rNLangle = 160;

struct Result{
  int moveUV;
  int moveIR;
  int moveNL;
  int cUV;
  int cIR;
  int cNL;
};

Result val;

void setup() {
  Serial.begin(115200);
  UVs.attach(UVPin);
  IRs.attach(IRPin);
  NLs.attach(NLPin);
  pinMode(testPin, OUTPUT);
  digitalWrite(testPin, HIGH);
  pinMode(esp_status_pin, OUTPUT);
  digitalWrite(esp_status_pin, HIGH);
  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
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
  bool activate = doc["activate"];
  bool testMode = doc["testMode"];
  int UVp = doc["uv_percent"];
  int IRp = doc["ir_percent"];
  int NLp = doc["natural_percent"];

  moveServo(UVp, IRp, NLp, activate, testMode);
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

int getPos(int pos){
  switch(pos){
    case 0:
      return 0;
    case 10:
      return 1;
      break;
    case 20:
      return 2;
      break;
    case 30:
      return 3;
      break;
    case 40:
      return 4;
      break;
    case 50:
      return 5;
      break;
    case 60:
      return 6;
      break;
    case 70:
      return 7;
      break;
    case 80:
      return 8;
      break;
    case 90:
      return 9;
      break;    
    case 100:
      return 10;
      break;
    case -10:
      return -1;
      break;
    case -20:
      return -2;
      break;
    case -30:
      return -3;
      break;
    case -40:
      return -4;
      break;
    case -50:
      return -5;
      break;
    case -60:
      return -6;
      break;
    case -70:
      return -7;
      break;
    case -80:
      return -8;
      break;
    case -90:
      return -9;
      break;    
    case -100:
      return -10;
      break;
  }
}

void turnOn(){
  turnR(0, 1, currentUV);
  turnR(0, 2, currentIR);
  turnR(0, 3, currentNL);
}

void turnOff(){
  turnL(currentUV, 1, currentUV);
  turnL(currentIR, 2, currentIR);
  turnL(currentNL, 3, currentNL);
}


Result translate(int UV, int IR, int NL){
    int desireUV = getPos(UV);
    int desireIR = getPos(IR);
    int desireNL = getPos(NL);
    Result result;
    result.moveUV = desireUV - currentUV;
    result.moveIR = desireIR - currentIR;
    result.moveNL = desireNL - currentNL;
    result.cUV = desireUV;
    result.cIR = desireIR;
    result.cNL = desireNL;
//    Serial.println(currentUV);

//Serial.println("passed 2" + result.moveUV + " : " + currentUV);
    return result;
  }

void turnR(int pos, int lightType, int count){
  Serial.println("-----------------right-----------------");
  Serial.println(pos); 
  Serial.println(lightType);
  Serial.println(count);
  Serial.println("----------------------------------");
  for (int counts = 0; counts < count; counts++){
    Serial.println("right");
    Serial.println(lightType);
    Serial.println(pos); 
    if(pos <= 10 && pos >= 0){
      switch(lightType){
        case 1:
          UVs.write(100);
          delay(200);
          UVs.write(180);
          delay(rUVangle);
          UVs.write(90);
          delay(1500);
          break;
        case 2:
          IRs.write(100);
          delay(200);
          IRs.write(180);
          delay(rIRangle);
          IRs.write(90);
          delay(1500);
          break;
        case 3:
          NLs.write(100);
          delay(200);
          NLs.write(180);
          delay(rNLangle);
          NLs.write(90);
          delay(1500);
          break;
      }
      pos++;
    }
  }
}

void turnL(int pos, int lightType, int count){
    Serial.println("------------------left--------------");
    Serial.println(pos); 
    Serial.println(lightType);
    Serial.println(count);
    Serial.println("----------------------------------");
    for (int counts = 0; counts < count; counts++){
      Serial.println("left");
      Serial.println(lightType); 
      Serial.println(pos); 
      if(pos <= 10 && pos >= 0){
        
        switch(lightType){
          case 1:
 
            UVs.write(1);
            delay(rUVangle);
            UVs.write(90);
            delay(1500);
            break;
          case 2:
            IRs.write(1);
            delay(rIRangle);
            IRs.write(90);
            delay(1500);
            break;
          case 3:
            NLs.write(1);
            delay(rNLangle);
            NLs.write(90);
            delay(1500);
            break;
            
        }
        pos--;  
      }
    } 
}


void moveServo(int UV, int IR, int NL, bool isActivate, bool testMode){
  Serial.println("-----------------------------------");
  Serial.println("moveServo");
  Serial.print("UV:");
  Serial.println(UV);
  Serial.print("IR:");
  Serial.println(IR);
  Serial.print("NL:");
  Serial.println(NL);
  Serial.println(isActivate);
  Serial.println("-----------------------------------");
  if(testMode){
    
    if(getPos(UV) >= 1){
      turnR(0, 1, getPos(UV)); 
    }
    else if(getPos(UV) < 0){
      turnL(10, 1, -getPos(UV));
    }
  
    if(getPos(IR) >= 1){
      //Serial.println("moved by : " + val.moveIR);  
      turnR(0, 2, getPos(IR));   
      
    }
    else if(getPos(IR) < 0){
      //Serial.println("-moved by : " + val.moveUV);
      turnL(10, 2, getPos(IR));
    }
  
    if(getPos(NL) >= 1){
      //Serial.println("moved by : " + val.moveNL);  
      turnR(0, 3, getPos(NL));   
      
    }
    else if(getPos(NL) < 0){
      //Serial.println("-moved by : " + val.moveUV);
      turnL(10, 3, getPos(NL));
    }
  }
  else{
    if(isActivate){
    
    Result val = translate(UV, IR, NL);  
    
    if(!currentState){
      turnOn();
      currentState = 1;
      Serial.println("turn on");
    }
    if(val.moveUV >= 1){
      turnR(currentUV, 1, val.moveUV); 
    }
    else if(val.moveUV < 0){
      turnL(currentUV, 1, -val.moveUV);
    }
  
    if(val.moveIR >= 1){
      //Serial.println("moved by : " + val.moveIR);  
      turnR(currentIR, 2, val.moveIR);   
      
    }
    else if(val.moveIR < 0){
      //Serial.println("-moved by : " + val.moveUV);
      turnL(currentIR, 2, -val.moveIR);
    }
  
    if(val.moveNL >= 1){
      //Serial.println("moved by : " + val.moveNL);  
      turnR(currentNL, 3, val.moveNL);   
      
    }
    else if(val.moveNL < 0){
      //Serial.println("-moved by : " + val.moveUV);
      turnL(currentNL, 3, -val.moveNL);
    }
    currentUV = val.cUV;
    currentIR = val.cIR;
    currentNL = val.cNL;
  }
  else if(!isActivate){
    turnOff();
    currentState = 0;
    Serial.println("turn off");
  }
  Serial.println("-----------------------------");
  Serial.print("current UV:");
  Serial.println(currentUV);
  Serial.print("current IR:");
  Serial.println(currentIR);
  Serial.print("current NL:");
  Serial.println(currentNL);
  Serial.println("-----------------------------");

  }
    
  String message;
  message += F("{\"action\": \"update/light\"");
  message += F(",\"espId\":");
  message += String(MQTT_SERIAL_RECEIVER_CH);
  message += F(",\"activate\":");
  message += String(isActivate);
  message += F("}");
  publishSerialData(message);

  Serial.println("moveServo:done");
}
