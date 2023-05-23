#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <ArduinoJson.h>


DynamicJsonDocument doc(1024);


#define DHTPIN 5          // Pin to which DHT11 sensor is connected
#define DHTTYPE DHT11     // DHT11 sensor type

/*******************Demo for MG-811 Gas Sensor Module V1.1*****************************
  Author:  Tiequan Shao: tiequan.shao@sandboxelectronics.com
         Peng Wei:     peng.wei@sandboxelectronics.com

  Lisence: Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

  Note:    This piece of source code is supposed to be used as a demostration ONLY. More
         sophisticated calibration is required for industrial field application.

                                                    Sandbox Electronics    2012-05-31
************************************************************************************/

/************************Hardware Related Macros************************************/
#define         MG_PIN                       (34)     //define which analog input channel you are going to use
//#define         BOOL_PIN                     (2)
#define         DC_GAIN                      (9)   //define the DC gain of amplifier

/***********************Software Related Macros************************************/
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interval(in milisecond) between each samples in 
//normal operation

/**********************Application Related Macros**********************************/
//These two values differ from sensor to sensor. user should derermine this value.
#define         ZERO_POINT_VOLTAGE           (1) //define the output of the sensor in volts when the concentration of CO2 is 400PPM
#define         REACTION_VOLTAGE            (12) //define the voltage drop of the sensor when move the sensor from air into 1000ppm CO2

/*****************************Globals***********************************************/
float           CO2Curve[3]  =  {2.602, ZERO_POINT_VOLTAGE, (REACTION_VOLTAGE / (2.602 - 3))};
//two points are taken from the curve.
//with these two points, a line is formed which is
//"approximately equivalent" to the original curve.
//data format:{ x, y, slope}; point1: (lg400, 0.324), point2: (lg4000, 0.280)
//slope = ( reaction voltage ) / (log400 –log1000)


DHT dht(DHTPIN, DHTTYPE); // Create DHT object

int count = 0;
int trigger = 0;
const int esp_status_pin = 2;
int send_time_interval = 60;
int trigger_interval = 300;

bool dehumidifier_status = false;

bool co2_status = false;

// Update these with values suitable for your network.
const char* ssid = "dlink-7F78";
const char* password = "qwertyuiop";
const char* mqtt_server = "192.168.0.10";
int minCO2 = 0;
int maxHumidity = 0;
#define mqtt_port 1883
#define MQTT_USER "admin"
#define MQTT_PASSWORD "password"
#define MQTT_SERIAL_PUBLISH_CH "python/mqtt"
#define MQTT_SERIAL_RECEIVER_CH "2"

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
  int input_co2 = doc["co2_threshold"];
  int input_humidity = doc["humidity_threshold"];

  if (input_co2 != 0) {
    minCO2 = input_co2;
  }

  if (input_humidity != 0) {
    maxHumidity = input_humidity;
  }

  update_threshold_to_db();
}

void update_threshold_to_db() {
  String updateThresholdData;
  updateThresholdData += F("{\"action\": \"update/threshold\"");
  updateThresholdData += F(",\"espId\":");
  updateThresholdData += String(MQTT_SERIAL_RECEIVER_CH);
  updateThresholdData += F(",\"humidity\":");
  updateThresholdData += String(maxHumidity);
  updateThresholdData += F(",\"co2\":");
  updateThresholdData += String(minCO2);
  updateThresholdData += F("}");
  publishSerialData(updateThresholdData);
}

void setup() {
  Serial.begin(115200);
  pinMode(esp_status_pin, OUTPUT);                        //set pin to input
  digitalWrite(esp_status_pin, HIGH);

  Serial.print("MG-811 Demostration\n");
  dht.begin();           // Initialize DHT sensor
  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
  setThreshold();
  Serial.print("Min CO2:");
  Serial.println(minCO2);
  Serial.print("Max Humidity\n");
  Serial.println(maxHumidity);

}

void setThreshold() {
  String thresholdRequest = "{\"action\":\"get/threshold\",\"espId\":";
  thresholdRequest += String(MQTT_SERIAL_RECEIVER_CH);
  thresholdRequest += F("}");
  publishSerialData(thresholdRequest);
}

float MGRead(int mg_pin)
{
  int i;
  float v = 0;

  for (i = 0; i < READ_SAMPLE_TIMES; i++) {
    v += analogRead(mg_pin);
    delay(READ_SAMPLE_INTERVAL);
  }
  v = (v / READ_SAMPLE_TIMES) * 5 / 1024 ;
  return v;
}

int  MGGetPercentage(float volts, float *pcurve)
{
  if ((volts / DC_GAIN ) >= ZERO_POINT_VOLTAGE) {
    return -1;
  } else {
    return pow(10, ((volts / DC_GAIN) - pcurve[1]) / pcurve[2] + pcurve[0]);
  }
}

void turnOnCo2() {
  String co2Request = F("{\"action\": \"turn_on/co2\",\"espId\":");
  co2Request += String(MQTT_SERIAL_RECEIVER_CH);
  co2Request += F("}");
  publishSerialData(co2Request);
}

void turnOffCo2() {
  String co2Request = F("{\"action\": \"turn_off/co2\",\"espId\":");
  co2Request += String(MQTT_SERIAL_RECEIVER_CH);
  co2Request += F("}");
  publishSerialData(co2Request);
}

void turnOnDehumidifier() {
  String dehumidifierRequest = F("{\"action\": \"turn_on/dehumidifier\",\"espId\":");
  dehumidifierRequest += String(MQTT_SERIAL_RECEIVER_CH);
  dehumidifierRequest += F("}");
  publishSerialData(dehumidifierRequest);
}

void turnOffDehumidifier() {
  String dehumidifierRequest = F("{\"action\": \"turn_off/dehumidifier\",\"espId\":");
  dehumidifierRequest += String(MQTT_SERIAL_RECEIVER_CH);
  dehumidifierRequest += F("}");
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

    int percentage;
    float volts;

    volts = MGRead(MG_PIN);
    Serial.print( "SEN-00007:" );
    Serial.print(volts);
    Serial.print( "V           " );

    percentage = MGGetPercentage(volts, CO2Curve);
    Serial.print("CO2:");
    if (percentage == -1) {
      Serial.print( "<400" );
    } else {
      Serial.print(percentage);
    }

    Serial.print( "ppm" );
    Serial.print("\n");

    if (!co2_status) {
      if (minCO2 > 0) {
        if (percentage < minCO2) {
          Serial.print("CO2 is over limit");
          turnOnCo2();
          Serial.println(minCO2);
          co2_status = true;
        }
      }
    }

    if (!dehumidifier_status) {
      if (maxHumidity > 0) {
        if (int(humidity) > maxHumidity) {
          Serial.print("Humidity is over limit");
          turnOnDehumidifier();
          Serial.println(maxHumidity);
          dehumidifier_status = true;
        }
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
    response += F(",\"co2\":");
    response += String(percentage);
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
  check_status();
  String message = collectAllSensorData();
  Serial.println("-------new message from broker-----");
  if (count == send_time_interval) {
    publishSerialData(message);
    count = 0;
    if (trigger == trigger_interval) {
      dehumidifier_status = false;
      co2_status = false;
      trigger = 0;
    }
  }
  Serial.println(count);
  count += 1;
  trigger += 1;
}
void check_status() {
  digitalWrite(esp_status_pin, HIGH);
  delay(500);
  digitalWrite(esp_status_pin, LOW);
  delay(500);
}
