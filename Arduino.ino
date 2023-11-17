#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

#include <Servo.h>



// Set these to run example.
#define FIREBASE_HOST "fir-topythonsample-default-rtdb.asia-southeast1.firebasedatabase.app"
#define FIREBASE_AUTH "ileju45ONNG2VSywdo0Iv5xU4sPkaKKvmphJzvGE"
#define WIFI_SSID "Redmi 8"
#define WIFI_PASSWORD "siva1234"

/*STATE 0-SPEECH RECOGNITION FAILED
  STATE 1-SPEECH RECOGNITION PASSED
  STATE 2-SPEECH DETECTION PASSED AND FACE DETECTION FAILED
  STATE 3-BOTH SPEECH RECOGNITON AND FACE DETECTION PASSED
*/

Servo servo;
int led=13;
int state=0;
FirebaseData Data;

void setup() {
  Serial.begin(9600);
  pinMode(16,OUTPUT);//D0-red
  pinMode(5,OUTPUT);//D1-blue
  pinMode(4,OUTPUT);//D2-green
  // Connect to Wifi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  Firebase.reconnectWiFi(true);
  delay(1000);
  //Firebase.setBool(Data,"/NewInst",false) ? NULL : Serial.println(Data.errorReason());
  //bool received = Firebase.getFloat(Data, "/NewInst") ? Data.to<bool>() ? true : false : Serial.println(Data.errorReason());
  //Serial.println(received);
  servo.attach(2); //D4
  servo.write(0);
}

void loop()
{

  int stage1 = Firebase.getInt(Data, "Stages/stage1") ? Data.to<int>() : Serial.println(Data.errorReason());
  int stage2 = Firebase.getInt(Data, "Stages/stage2") ? Data.to<int>() : Serial.println(Data.errorReason());

  Serial.print("STAGE 1=");
  Serial.println(stage1);
  Serial.print("STAGE 2=");
  Serial.println(stage2);
  if(stage1==0 && stage2==0){
    state=0;
    //TURNS THE LED RED
    digitalWrite(16,HIGH);  
    digitalWrite(5,LOW);  
    digitalWrite(4,HIGH); 
    servo.write(0);
  }
  else if(stage1==1 && stage2==0){
    state=1;
    //TURNS THE LED BLUE
    digitalWrite(16,LOW);  
    digitalWrite(5,HIGH);  
    digitalWrite(4,HIGH); 
    servo.write(0);  

    
  }
  else if(stage1==1 && stage2==1){
    state=2;
    //green
    digitalWrite(16,HIGH);  
    digitalWrite(5,HIGH);  
    digitalWrite(4,LOW);  
    servo.write(90);
  }
  else
    //digitalWrite(16,HIGH);  
    //digitalWrite(5,HIGH);  
    //digitalWrite(4,HIGH);
    Serial.println("INVALID");
  }
  delay(5000);

}
