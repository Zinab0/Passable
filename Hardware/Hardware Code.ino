#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_now.h>
#include <ArduinoJson.h>


const String serverAddress = "http://172.20.10.2:8000";
const char* ssid = "Zinab"; // wifi ssid ->  WiFi network name
const char* password = "zozozozo";  // wifi_password


//char JSONMSG[]=" {'is_accident': 0, 'traffic_density': 'Low', 'new_green_light_time': 4000}"; //Original message
// Define light ports
// --- TL 1 ---
#define TL1_G  23
#define TL1_Y  22
#define TL1_R  21
// --- TL 2 ---
#define TL2_G  17
#define TL2_Y  18
#define TL2_R  19
// --- TL 3 ---
#define TL3_G  25
#define TL3_Y  26
#define TL3_R  27
// --- TL 4 ---
#define TL4_G  14
#define TL4_Y  12
#define TL4_R  13

// MAC Address of responder - edit as required
uint8_t broadcastAddress001[] = {0x48, 0xE7, 0x29, 0xAC, 0x90, 0xF0};
uint8_t broadcastAddress010[] = {0x48, 0xE7, 0x29, 0xB6, 0xFB, 0xE4};
uint8_t broadcastAddress011[] = {0x48, 0xE7, 0x29, 0xB6, 0x72, 0xB4};
uint8_t broadcastAddress100[] = {0x48, 0xE7, 0x29, 0xAD, 0x12, 0x94};
uint8_t broadcastAddress101[] = {0x48, 0xE7, 0x29, 0xB6, 0xF6, 0x18};

// Define a data structure
typedef struct struct_message {
  char a[32];
} struct_message;
 

// Variables for test data
  String Alert;
  String trafficDensity;
  int defaultRed = 1500;
  int defaultYellow = 1000;
  int defaultGreen = 5000;
  int isAccident= 0;
  int isCongestion=0;
  int newGreenLightTime;

// Create a structured object
  struct_message congestionAlert;
  struct_message accidentAlert;

// Peer info
  esp_now_peer_info_t peerInfo001;
  esp_now_peer_info_t peerInfo010;
  esp_now_peer_info_t peerInfo011;
  esp_now_peer_info_t peerInfo100;
  esp_now_peer_info_t peerInfo101;

// Callback function called when data is sent
  void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.print("\r\nLast Packet Send Status:\t");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
  }


////////////// TRIAL 1 //////////////


void setup() {

  Serial.begin(115200);
  
//Connecting to wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(3000);
    Serial.println("Connecting to WiFi...");
  } Serial.println("Connected to WiFi");

// Set up pins
  pinMode(TL1_G, OUTPUT);
  pinMode(TL1_Y, OUTPUT);
  pinMode(TL1_R, OUTPUT);
  pinMode(TL2_G, OUTPUT);
  pinMode(TL2_Y, OUTPUT);
  pinMode(TL2_R, OUTPUT);
  pinMode(TL3_G, OUTPUT);
  pinMode(TL3_Y, OUTPUT);
  pinMode(TL3_R, OUTPUT);
  pinMode(TL4_G, OUTPUT);
  pinMode(TL4_Y, OUTPUT);
  pinMode(TL4_R, OUTPUT);

// Set ESP32 as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
 
// Initilize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
 
// Register the send callback
  esp_now_register_send_cb(OnDataSent);

// Register peer 1
  memcpy(peerInfo001.peer_addr, broadcastAddress001, 6);
  peerInfo001.channel = 0;  
  peerInfo001.encrypt = false;
  // Add peer        
  if (esp_now_add_peer(&peerInfo001) != ESP_OK){
    Serial.println("Failed to add peer 001");
    return;
  }

// Register peer 2
  memcpy(peerInfo010.peer_addr, broadcastAddress010, 6);
  peerInfo010.channel = 0;  
  peerInfo010.encrypt = false;
  // Add peer        
  if (esp_now_add_peer(&peerInfo010) != ESP_OK){
    Serial.println("Failed to add peer 010");
    return;
  }

 // Register peer 3
  memcpy(peerInfo011.peer_addr, broadcastAddress011, 6);
  peerInfo011.channel = 0;  
  peerInfo011.encrypt = false;
  // Add peer        
  if (esp_now_add_peer(&peerInfo011) != ESP_OK){
    Serial.println("Failed to add peer 011");
    return;
  }

// Register peer 4
  memcpy(peerInfo100.peer_addr, broadcastAddress100, 6);
  peerInfo100.channel = 0;  
  peerInfo100.encrypt = false;
  // Add peer        
  if (esp_now_add_peer(&peerInfo100) != ESP_OK){
    Serial.println("Failed to add peer 100");
    return;
  }

// Register peer 5
  memcpy(peerInfo101.peer_addr, broadcastAddress101, 6);
  peerInfo101.channel = 0;  
  peerInfo101.encrypt = false;
  // Add peer        
  if (esp_now_add_peer(&peerInfo101) != ESP_OK){
    Serial.println("Failed to add peer 101");
    return;
  }

}

void loop() {

// Format structured data
  strcpy(congestionAlert.a, "Congestion Ahead!!");
  strcpy(accidentAlert.a, "Accident Ahead!!");

String payload = getTrafficInformation();
//-------------------------------------------------------------------

// Parse JSON payload
  DynamicJsonDocument doc(1024);
  DeserializationError error1 = deserializeJson(doc, payload);
  if (error1) {
    Serial.print("Error parsing JSON1: ");
    Serial.println(error1.c_str());
    return;
  }

// Extract values from JSON
  isAccident = doc["is_accident"];
  trafficDensity = doc["traffic_density"].as<String>();
  newGreenLightTime = doc["new_green_light_time"];

  if(trafficDensity=="High" || trafficDensity=="Moderate"){
    isCongestion=1;
  }
// print values extracted from JSON
  Serial.println("TL 1");
  Serial.println("isAccident: "+ String(isAccident)); // maybe it won't work as function in function, try to print w/ string
  Serial.println("trafficDensity: " + String(trafficDensity));
  Serial.println("isCongestion: " + String(isCongestion));
  Serial.println("newGreenLightTime: " + String(newGreenLightTime));

  
// Send Congestion alert to vehicles
  if(isCongestion == 1){
    esp_err_t result001 = esp_now_send(broadcastAddress001, (uint8_t *) &congestionAlert, sizeof(congestionAlert));
    if (result001 == ESP_OK) {
      Serial.println("Sending confirmed 001");
    }else {
     Serial.println("Sending error 001"); }

  }
// Send Accident alert to vehicles
  else if(isAccident == 1){
    esp_err_t result001 = esp_now_send(broadcastAddress001, (uint8_t *) &accidentAlert, sizeof(accidentAlert));
    if (result001 == ESP_OK) {
      Serial.println("Sending confirmed 001");
    } else {
     Serial.println("Sending error 001"); }
  }
openTL1(newGreenLightTime);

//-------------------------------------------------------------------

// Parse JSON payload
  //DynamicJsonDocument doc(1024);
  DeserializationError error2 = deserializeJson(doc, payload);
  if (error2) {
    Serial.print("Error parsing JSON2: ");
    Serial.println(error2.c_str());
    return;
  }

// Extract values from JSON
  isAccident = doc["is_accident"];
  trafficDensity = doc["traffic_density"].as<String>();
  newGreenLightTime = doc["new_green_light_time"];

  if(trafficDensity=="High" || trafficDensity=="Moderate"){
    isCongestion=1;
  }

  Serial.println("isAccident: "+ String(isAccident)); // maybe it won't work as function in function, try to print w/ string 
  Serial.println("trafficDensity: " + String(trafficDensity));
  Serial.println("isCongestion: " + String(isCongestion));
  Serial.println("newGreenLightTime: " + String(newGreenLightTime));

// Send congestion alert to vehicles
  if(isCongestion == 1){
    esp_err_t result010 = esp_now_send(broadcastAddress010, (uint8_t *) &congestionAlert, sizeof(congestionAlert));
    if (result010 == ESP_OK) {
      Serial.println("Sending confirmed 010");
    }
    else {
     Serial.println("Sending error 010");
    }

  }
// Send alert to vehicles
  else if(isAccident == 1){
    esp_err_t result010 = esp_now_send(broadcastAddress010, (uint8_t *) &accidentAlert, sizeof(accidentAlert));
    if (result010 == ESP_OK) {
      Serial.println("Sending confirmed 010");
    }
    else {
     Serial.println("Sending error 010");
    }
  }
openTL2(newGreenLightTime);

//-------------------------------------------------------------------

  // Determine incident type
  // Parse JSON payload
  //DynamicJsonDocument doc(1024);
  DeserializationError error3 = deserializeJson(doc, payload);
  if (error3) {
    Serial.print("Error parsing JSON3: ");
    Serial.println(error3.c_str());
    return;
  }

// Extract values from JSON
  isAccident = doc["is_accident"];
  trafficDensity = doc["traffic_density"].as<String>();
  newGreenLightTime = doc["new_green_light_time"];

  if(trafficDensity=="High" || trafficDensity=="Moderate"){
    isCongestion=1;
  }

  Serial.println("TL 3");
  Serial.println("isAccident: "+ String(isAccident)); 
  Serial.println("trafficDensity: " + String(trafficDensity));
  Serial.println("isCongestion: " + String(isCongestion));
  Serial.println("newGreenLightTime: " + String(newGreenLightTime));

// Send Congsetion alert to vehicles
  if(isCongestion == 1){
    esp_err_t result011 = esp_now_send(broadcastAddress011, (uint8_t *) &congestionAlert, sizeof(congestionAlert));
    if (result011 == ESP_OK) {
      Serial.println("Sending confirmed 011");
    }
    else {
     Serial.println("Sending error 011");
    }
  }
// Send accident  alert to vehicles
  else if(isAccident == 1){
    
    esp_err_t result011 = esp_now_send(broadcastAddress011, (uint8_t *) &accidentAlert, sizeof(accidentAlert));
    if (result011 == ESP_OK) {
      Serial.println("Sending confirmed 011");
    }
    else {
     Serial.println("Sending error 011");
    }
  }
openTL3(newGreenLightTime);

//-------------------------------------------------------------------
  
// Parse JSON payload
  //DynamicJsonDocument doc(1024);
  DeserializationError error4 = deserializeJson(doc, payload);
  if (error4) {
    Serial.print("Error parsing JSON4: ");
    Serial.println(error4.c_str());
    return;
  }

// Extract values from JSON
  isAccident = doc["is_accident"];
  trafficDensity = doc["traffic_density"].as<String>();
  newGreenLightTime = doc["new_green_light_time"];
  if(trafficDensity=="High" || trafficDensity=="Moderate"){
    isCongestion=1;
  }

  
  Serial.println("TL 3");
  Serial.println("isAccident: "+ String(isAccident)); 
  Serial.println("trafficDensity: " + String(trafficDensity));
  Serial.println("isCongestion: " + String(isCongestion));
  Serial.println("newGreenLightTime: " + String(newGreenLightTime));


// Send congestion alert to vehicles
  if(isCongestion == 1){
    esp_err_t result100 = esp_now_send(broadcastAddress100, (uint8_t *) &congestionAlert, sizeof(congestionAlert));
    if (result100 == ESP_OK) {
      Serial.println("Sending confirmed 100");
    }
    else {
     Serial.println("Sending error 100");
    }
    esp_err_t result101 = esp_now_send(broadcastAddress101, (uint8_t *) &congestionAlert, sizeof(congestionAlert));
    if (result101 == ESP_OK) {
      Serial.println("Sending confirmed 101");
    }
    else {
     Serial.println("Sending error 101");
    }
  }
// Send accident alert to vehicles
  else if(isAccident == 1){
    esp_err_t result100 = esp_now_send(broadcastAddress100, (uint8_t *) &accidentAlert, sizeof(accidentAlert));
    if (result100 == ESP_OK) {
      Serial.println("Sending confirmed 100");
    }
    else {
     Serial.println("Sending error 100");
    }
    esp_err_t result101 = esp_now_send(broadcastAddress101, (uint8_t *) &accidentAlert, sizeof(accidentAlert));
    if (result101 == ESP_OK) {
      Serial.println("Sending confirmed 101");
    }
    else {
     Serial.println("Sending error 101");
    }
  }

openTL4(newGreenLightTime);
  

  delay(5000);  // Fetch traffic information every 5 seconds
}

String getTrafficInformation() {
  String payload;
  String url = serverAddress + "/get_traffic_information/";
  HTTPClient http;
  http.begin(url);
  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    if (http.getSize() > 0) {
      payload = http.getString();
      Serial.println("Received traffic information: " + payload);
    } else {
      Serial.println("No traffic information received");
    }
  } else {
    Serial.print("Error in HTTP request: ");
    Serial.println(httpResponseCode);
  }
  http.end();
  return payload;
}

// Open traffic light functions
void openTL1(int newGreenLightTime){
  digitalWrite(TL1_R, LOW);
  digitalWrite(TL1_G, HIGH);
  digitalWrite(TL2_R, HIGH);
  digitalWrite(TL3_R, HIGH);
  digitalWrite(TL4_R, HIGH);
  delay(newGreenLightTime);
  digitalWrite(TL1_G, LOW);
  digitalWrite(TL1_Y, HIGH);
  delay(defaultYellow);
  digitalWrite(TL1_Y, LOW);
}
void openTL2(int newGreenLightTime){
  digitalWrite(TL2_R, LOW);
  digitalWrite(TL1_R, HIGH);
  digitalWrite(TL2_G, HIGH);
  digitalWrite(TL3_R, HIGH);
  digitalWrite(TL4_R, HIGH);
  delay(defaultGreen);
  digitalWrite(TL2_G, LOW);
  digitalWrite(TL2_Y, HIGH);
  delay(defaultYellow);
  digitalWrite(TL2_Y, LOW);
}

void openTL3(int newGreenLightTime){
  digitalWrite(TL3_R, LOW);
  digitalWrite(TL1_R, HIGH);
  digitalWrite(TL2_R, HIGH);
  digitalWrite(TL3_G, HIGH);
  digitalWrite(TL4_R, HIGH);
  delay(defaultGreen);
  digitalWrite(TL3_G, LOW);
  digitalWrite(TL3_Y, HIGH);
  delay(defaultYellow);
  digitalWrite(TL3_Y, LOW);
}

void openTL4(int newGreenLightTime){
  digitalWrite(TL4_R, LOW);
  digitalWrite(TL1_R, HIGH);
  digitalWrite(TL2_R, HIGH);
  digitalWrite(TL3_R, HIGH);
  digitalWrite(TL4_G, HIGH);
  delay(defaultGreen);
  digitalWrite(TL4_G, LOW);
  digitalWrite(TL4_Y, HIGH);
  delay(defaultYellow);
  digitalWrite(TL4_Y, LOW);
}