#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
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

Adafruit_BNO055 bno = Adafruit_BNO055(55);

int pot;
int out;
float angle = 0.00;
String prev_command="";
int cacca = 0;

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
  
  delay(1000);
    
  bno.setExtCrystalUse(true);
}
 
void loop() {
  sensors_event_t event; 
  bno.getEvent(&event); 
  if(prev_command=="w"){
    float currentAngle = event.orientation.x;
    float yangle = event.orientation.y;
    Serial.print(yangle);
    if(yangle>2 || yangle<-2){
      cacca=cacca+1;
      Serial.print("inclinato");
    }
    Serial.print(" cacca");
    Serial.print(cacca);
    if(cacca>500 && (yangle<2 && yangle>-2)){
      Serial.print("non più inclinato");
      delay(700);
      cacca=0;
      stop();
      prev_command="q";
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
        if(currentAngle<angle+0.3 && currentAngle>angle-0.3){
          analogWrite(MD_PWM1, 100);
          analogWrite(MD_PWM2, 100);
          analogWrite(MA_PWM1, 100);
          analogWrite(MA_PWM2, 100);
        }else if(currentAngle>angle+3){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 30);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 30);
        }else if(currentAngle<angle-3){
          analogWrite(MD_PWM2, 30);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 30);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle>angle+1){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 50);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 50);
        }else if(currentAngle<angle-1){
          analogWrite(MD_PWM2, 50);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 50);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle>angle+0.5){
          analogWrite(MD_PWM2, 60);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 60);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle<angle-0.5){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 60);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 60);
        }else if(currentAngle>angle+0.3){
          analogWrite(MD_PWM2, 70);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 70);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle<angle-0.3){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 70);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 70);
        }else if(currentAngle>angle+0.2){
          analogWrite(MD_PWM2, 80);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 80);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle<angle-0.2){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 80);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 80);
        }else if(currentAngle>angle+0.1){
          analogWrite(MD_PWM2, 90);
          analogWrite(MD_PWM1, 100);
          analogWrite(MA_PWM2, 90);
          analogWrite(MA_PWM1, 100);
        }else if(currentAngle<angle-0.1){
          analogWrite(MD_PWM2, 100);
          analogWrite(MD_PWM1, 90);
          analogWrite(MA_PWM2, 100);
          analogWrite(MA_PWM1, 90);
        }    
    Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.println(currentAngle);
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
      if(currentAngle<angle+0.3 && currentAngle>angle-0.3){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle>angle+3){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 30);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 30);
      }else if(currentAngle<angle-3){
        analogWrite(MD_PWM1, 30);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 30);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle>angle+1){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 50);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 50);
      }else if(currentAngle<angle-1){
        analogWrite(MD_PWM1, 50);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 50);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle>angle+0.5){
        analogWrite(MD_PWM1, 60);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 60);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle<angle-0.5){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 60);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 60);
      }else if(currentAngle>angle+0.3){
        analogWrite(MD_PWM1, 70);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 70);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle<angle-0.3){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 70);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 70);
      }else if(currentAngle>angle+0.2){
        analogWrite(MD_PWM1, 80);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 80);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle<angle-0.2){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 80);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 80);
      }else if(currentAngle>angle+0.1){
        analogWrite(MD_PWM1, 90);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 90);
        analogWrite(MA_PWM2, 100);
      }else if(currentAngle<angle-0.1){
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 90);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 90);
      }
    Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.println(currentAngle);
      
  }else if(prev_command=="a" || prev_command=="d" || prev_command=="r")
  {
    float currentAngle = event.orientation.x;
    if(currentAngle>=270){
      if(angle==0){
        angle=360;
      }
    }else if(currentAngle<270){
      if(angle==360){
        angle=0;
      }
    }
    float angledifference = angle - currentAngle;

    Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print("   Current: ");
    Serial.print(currentAngle);
    Serial.print("   Difference: ");
    Serial.println(angledifference);

    if (angledifference < -10 || angledifference > 10) {
        analogWrite(MD_PWM1, 100);
        analogWrite(MD_PWM2, 100);
        analogWrite(MA_PWM1, 100);
        analogWrite(MA_PWM2, 100);
    } else if ((angledifference >= -10 || angledifference <= 10) && (angledifference < -5 || angledifference > 5)) {
        analogWrite(MD_PWM1, 30);
        analogWrite(MD_PWM2, 30);
        analogWrite(MA_PWM1, 30);
        analogWrite(MA_PWM2, 30);
    } else if ((angledifference >= -5 || angledifference <= 5) && (angledifference < -0.1 || angledifference > 0.1)) {
        analogWrite(MD_PWM1, 20);
        analogWrite(MD_PWM2, 20);
        analogWrite(MA_PWM1, 20);
        analogWrite(MA_PWM2, 20);
    } else if (angledifference == 0.0) {
        stop();
        prev_command="q";
        Serial.println("Complete");
    }
    
  }

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    float yangle = event.orientation.y;
    if (data.length() > 0) { // Check if there is any valid data
      if(cacca==true && data[0]=='w'){
        Serial.println("mao");
      }else{
        switch (data[0]) {
        case 'w':
          avanti();
          prev_command="w";
          break;
        case 'q':
          if(cacca==0){
            stop();
            prev_command="q";
          }
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
          if(currentAngle-angle<0){
            destra();
          }else{
            sinistra();
          }
          angle=angle;
          if(angle>=360){
            angle=angle-360;
          }else if(angle<0){
            angle=angle+360;
          }
          prev_command="r";
        default:
          // Handle unknown command or do nothing
          break;
        }
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