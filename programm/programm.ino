#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include "Adafruit_TCS34725.h"
//motori dietro
#define MD_PWM1 9
#define MD_AIN2 8
#define MD_AIN1 7
#define MD_PWM2 10
#define MD_BIN1 11
#define MD_BIN2 12
#define MD_STB 13
//motori davanti
#define MA_PWM1 5
#define MA_PWM2 6
#define MA_BIN1 3
#define MA_BIN2 4
#define MA_STB 2


#define redpin 14
#define greenpin 15
#define bluepin 16


#define commonAnode true

#define COLOR_blu 100
#define COLOR_nero 124

// our RGB -> eye-recognized gamma color
byte gammatable[256];


Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

Adafruit_BNO055 bno = Adafruit_BNO055(55);

int pot;
int out;
float angle = 0.00;
String prev_command="";
int cacca = 0;
int scoreggia=0;
bool blu=false;
bool nero=false;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
  pinMode(MD_PWM1,OUTPUT);
  pinMode(MD_AIN1,OUTPUT);
  pinMode(MD_AIN2,OUTPUT);
  pinMode(MD_PWM2,OUTPUT);
  pinMode(MD_BIN1,OUTPUT);
  pinMode(MD_BIN2,OUTPUT);
  pinMode(MD_STB, OUTPUT);
  digitalWrite(MD_STB, HIGH);
  pinMode(MA_PWM1,OUTPUT);
  pinMode(MA_PWM2,OUTPUT);
  pinMode(MA_BIN1,OUTPUT);
  pinMode(MA_BIN2,OUTPUT);
  pinMode(MA_STB, OUTPUT);
  digitalWrite(MA_STB, HIGH);
  while (!Serial);

  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  if (tcs.begin()) {
    //Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1); // halt!
  }
  delay(1000);

  #if defined(ARDUINO_ARCH_ESP32)
    ledcAttach(redpin, 12000, 8);
    ledcAttach(greenpin, 12000, 8);
    ledcAttach(bluepin, 12000, 8);
  #else
    pinMode(redpin, OUTPUT);
    pinMode(greenpin, OUTPUT);
    pinMode(bluepin, OUTPUT);
  #endif


  for (int i=0; i<256; i++) {
    float x = i;
    x /= 255;
    x = pow(x, 2.5);
    x *= 255;

    if (commonAnode) {
      gammatable[i] = 255 - x;
    } else {
      gammatable[i] = x;
    }
    //Serial.println(gammatable[i]);
  }

  bno.setExtCrystalUse(true);
}
 
void loop() {
  sensors_event_t event; 
  bno.getEvent(&event); 
  float red, green, blue;
  tcs.getRGB(&red, &green, &blue);
  if(prev_command=="w"){
    float currentAngle = event.orientation.x;
    float yangle = event.orientation.y;  
    //Serial.print(yangle);
    //Serial.println(int(red));
    if(blu==true){
      Serial.println("Blu");
      blu=false;
    }else if(nero==true){
      Serial.println("Nero");
      nero=false;
    }else{
      Serial.println("BIANCOS");
    }
    if(COLOR_blu<int(blue)){
      blu=true;      
    }
    if(COLOR_nero-3<int(red) && COLOR_nero+3>int(red)){
      stop();
      prev_command="q";
      nero=true;
    }else{
      if(cacca==0 &&(yangle>6 || yangle<-6)){
      cacca=1;
      Serial.println("inclinato");
    }
    if(cacca==1 &&(yangle<2 && yangle>-2)){
      cacca=0;
      Serial.println("completata salita");
    }else{
      if(currentAngle>270){
        if(angle==0){
          angle=360;
        }
      }else if(currentAngle<270){
        if(angle==360){
          angle=0;
        }
      }
      if(currentAngle==angle){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle>angle+3){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 100);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 100);
      }else if(currentAngle<angle-3){
        analogWrite(MD_PWM2, 100);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 100);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle>angle+1){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 130);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 130);
      }else if(currentAngle<angle-1){
        analogWrite(MD_PWM2, 130);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 130);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle>angle+0.5){
        analogWrite(MD_PWM2, 150);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 150);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle<angle-0.5){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 150);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 150);
      }else if(currentAngle>angle+0.3){
        analogWrite(MD_PWM2, 170);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 170);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle<angle-0.3){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 170);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 170);
      }else if(currentAngle>angle+0.2){
        analogWrite(MD_PWM2, 180);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 180);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle<angle-0.2){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 190);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 190);
      }else if(currentAngle>angle+0.1){
        analogWrite(MD_PWM2, 190);
        analogWrite(MD_PWM1, 200);
        analogWrite(MA_PWM2, 190);
        analogWrite(MA_PWM1, 200);
      }else if(currentAngle<angle-0.1){
        analogWrite(MD_PWM2, 200);
        analogWrite(MD_PWM1, 190);
        analogWrite(MA_PWM2, 200);
        analogWrite(MA_PWM1, 190);
      }    
 /*   Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.println(currentAngle);*/
      }
    }
  }
  else if(prev_command=="s")
  {
    float currentAngle = event.orientation.x;
    if(currentAngle>270){
      if(angle==0){
        angle=360;
      }
    }else if(currentAngle<270){
      if(angle==360){
        angle=0;
      }
    }
      if(currentAngle==angle){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle>angle+3){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle<angle-3){
        analogWrite(MD_PWM1, 30);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 30);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle>angle+1){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 130);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 130);
      }else if(currentAngle<angle-1){
        analogWrite(MD_PWM1, 130);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 130);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle>angle+0.5){
        analogWrite(MD_PWM1, 150);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 150);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle<angle-0.5){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 150);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 150);
      }else if(currentAngle>angle+0.3){
        analogWrite(MD_PWM1, 170);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 170);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle<angle-0.3){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 170);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 170);
      }else if(currentAngle>angle+0.2){
        analogWrite(MD_PWM1, 180);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 180);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle<angle-0.2){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 180);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 180);
      }else if(currentAngle>angle+0.1){
        analogWrite(MD_PWM1, 190);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 190);
        analogWrite(MA_PWM2, 200);
      }else if(currentAngle<angle-0.1){
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 190);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 190);
      }
   /* Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.println(currentAngle); */
      
  }else if(prev_command=="a" || prev_command=="d" || prev_command=="r")
  {
    float currentAngle = event.orientation.x;
    if(currentAngle>=180){
      if(angle==0){
        angle=360;
      }
    }else if(currentAngle<180){
      if(angle==360){
        angle=0;
      }
    }
    if(angle>=360){
      angle=angle-360;
    }else if(angle<0){
      angle=angle+360;
    }
    Serial.print(angle);
    Serial.print("  ");
    Serial.println(currentAngle);
    float angledifference = angle - currentAngle;
    if(angle==0 && (currentAngle<360 && currentAngle>270)){
      destra();
    }else if(angle==0 && (currentAngle>0 && currentAngle<=90)){
      sinistra();
    }else if(angle==90 && (currentAngle<90 && currentAngle>0)){
      destra();
    }else if(angle==90 && (currentAngle>90 && currentAngle<=180)){
      sinistra();
    }else if(angle==180 && (currentAngle<180 && currentAngle>90)){
      destra();
    }else if(angle==180 && (currentAngle>180 && currentAngle<=270)){
      sinistra();
    }else if(angle==270 && (currentAngle<270 && currentAngle>180)){
      destra();
    }else if(angle==270 && (currentAngle>270 && currentAngle<=359)){
      sinistra();
    }else if(angle==360 && (currentAngle<270 && currentAngle>180)){
      destra();
    }else if(angle==360 && (currentAngle>270 && currentAngle<=359)){
      sinistra();
    }
 /*   Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.print(currentAngle);
    Serial.print("   Difference: ");
    Serial.println(angledifference); */

    if (angledifference < -10 || angledifference > 10) {
        analogWrite(MD_PWM1, 200);
        analogWrite(MD_PWM2, 200);
        analogWrite(MA_PWM1, 200);
        analogWrite(MA_PWM2, 200);
    } else if ((angledifference >= -10 || angledifference <= 10) && (angledifference < -5 || angledifference > 5)) {
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 100);
    } else if ((angledifference >= -5 || angledifference <= 5) && (angledifference < -1 || angledifference > 1)) {
        analogWrite(MD_PWM1, 40);
        analogWrite(MD_PWM2, 40);
        analogWrite(MA_PWM1, 40);
        analogWrite(MA_PWM2, 40);
    } else{
        stop();
        prev_command="q";
        Serial.println("Complete");
    }
    
  }else if(prev_command=="q"){
    if(blu==true){
      Serial.println("Blu");
      blu=false;
    }else if(nero==true){
      Serial.println("Nero");
      nero=false;
    }else{
      Serial.println("BIANCOS");
    }
  }

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    float yangle = event.orientation.y;
    if (data.length() > 0) {
        switch (data[0]) {
        case 'w':
          avanti();
          prev_command="w";
          break;
        case 'q':
          stop();
          prev_command="q";
          break;
        case 's':
          indietro();
          prev_command="s";
          break;
        case 'a':
          sinistra();
          prev_command="a";
          angle=angle-90;
          if(angle>=360){
            angle=angle-360;
          }else if(angle<0){
            angle=angle+360;
          }
          break;
        case 'd':
          destra();
          prev_command="d";
          angle=angle+90;
          if(angle>=360){
            angle=angle-360;
          }else if(angle<0){
            angle=angle+360;
          }
          break;
        case 'r':
          float currentAngle = event.orientation.x;
          if(angle>=360){
            angle=angle-360;
          }else if(angle<0){
            angle=angle+360;
          }
          Serial.println(currentAngle);
          Serial.println(angle);
          if(angle==0 && (currentAngle<=360 && currentAngle>270)){
            destra();
          }else if(angle==0 && (currentAngle>0 && currentAngle<=90)){
            sinistra();
          }else if(angle==90 && (currentAngle<90 && currentAngle>0)){
            destra();
          }else if(angle==90 && (currentAngle>90 && currentAngle<=180)){
            sinistra();
          }else if(angle==180 && (currentAngle<180 && currentAngle>90)){
            destra();
          }else if(angle==180 && (currentAngle>180 && currentAngle<=270)){
            sinistra();
          }else if(angle==270 && (currentAngle<270 && currentAngle>180)){
            destra();
          }else if(angle==270 && (currentAngle>270 && currentAngle<=359)){
            sinistra();
          }
          
          prev_command="r";
        default:
          // Handle unknown command or do nothing
          break;
      }
      
    }
  }
}

void avanti(){
  digitalWrite(MD_AIN1,LOW);
  digitalWrite(MD_AIN2,HIGH);
  digitalWrite(MD_BIN1,LOW);
  digitalWrite(MD_BIN2,HIGH);
  digitalWrite(MA_BIN1,LOW);
  digitalWrite(MA_BIN2,HIGH);
}

void indietro(){
  digitalWrite(MD_AIN1,HIGH);
  digitalWrite(MD_AIN2,LOW);
  digitalWrite(MD_BIN1,HIGH);
  digitalWrite(MD_BIN2,LOW);
  digitalWrite(MA_BIN1,HIGH);
  digitalWrite(MA_BIN2,LOW);

}

void stop(){
  analogWrite(MD_PWM1,0);
  analogWrite(MD_PWM2,0); 
  analogWrite(MA_PWM1,0);
  analogWrite(MA_PWM2,0);
}

void destra(){
    digitalWrite(MD_AIN1,LOW);
    digitalWrite(MD_AIN2,HIGH);
    digitalWrite(MD_BIN1,HIGH);
    digitalWrite(MD_BIN2,LOW);
    digitalWrite(MA_BIN1,HIGH);
    digitalWrite(MA_BIN2,LOW);

}

void sinistra(){
    digitalWrite(MD_AIN1,HIGH);
    digitalWrite(MD_AIN2,LOW);
    digitalWrite(MD_BIN1,LOW);
    digitalWrite(MD_BIN2,HIGH);
    digitalWrite(MA_BIN1,LOW);
    digitalWrite(MA_BIN2,HIGH);
}