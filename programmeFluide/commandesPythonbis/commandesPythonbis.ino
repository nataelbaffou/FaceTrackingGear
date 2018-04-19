
#define PIN_MODE 100
#define DIGITAL_WRITE 101
#define DIGITAL_READ 102
#define ANALOG_WRITE 103
#define ANALOG_READ 104
#define SERVO_WRITE 105
#define SERVO_READ 106
#define SERVO_ATTACH 107
#define MAPPING 108

#include <Servo.h>

Servo monservo;
Servo monservo2;

unsigned long startTimestamp;
unsigned long timePos;
int ecartX = 0;
int ecartY = 0;
long distX = 0;
long distY = 0;
long tempsX = 0;
long tempsY = 0;
long angleX = 90;
long angleY = 90;
long angleDepX = 0;
long angleDepY = 0;
int invX = 1;
int invY = 1;
              
void setup() {
  char c;
  Serial.begin(500000);
  Serial.flush();
  c = 0;
  Serial.write(c);
  c = 255;
  Serial.write(c);
  c = 0;
  Serial.write(c);
}
              
void loop() {
  char commande;  
  if (Serial.available()>0) {
     commande = Serial.read();
     if (commande==MAPPING)commande_mapping();
     else if (commande==SERVO_WRITE) commande_servo_write();
     else if (commande==SERVO_ATTACH) commande_servo_attach();
     
  }
  if(0){
      timePos = int((millis() - startTimestamp));
      if(invX == 1){
        angleX = map(timePos, 0, tempsX*1000, angleDepX, angleDepX + 90);
      }
      else{
        angleX = map(timePos, 0, tempsX*1000, angleDepX, angleDepX - 90);
      }
      monservo.write(angleX);
      if(invY == 1){
        angleY = map(timePos, 0, tempsY*1000, angleDepY, angleDepY + 90);
      }
      else{
        angleY = map(timePos, 0, tempsY*1000, angleDepY, angleDepY - 90);
      }
      monservo2.write(angleY);
  }
  
}

void commande_mapping() {
    ecartX = 0;
    ecartY = 0;
    for(int i=0; i<5; i++)
    {
      while (Serial.available()<1);
      ecartX = ecartX + Serial.read() * pow(10, 5-i) / 10;
    }
    for(int i=0; i<5; i++)
    {
      while (Serial.available()<1);
      ecartY = ecartY + Serial.read() * pow(10, 5-i) / 10;
    }
    while (Serial.available()<1);
    invX = Serial.read();

    while (Serial.available()<1);
    invX = Serial.read();
    
    // vitesse = ecart*90/240
    // temps = dist / vitesse = 90 / ecart * 90 / 240 = 240 / ecart
    tempsX = 240/ecartX;
    angleDepX = angleX;

    tempsY = 320/ecartY;
    angleDepY = angleY;
    
    startTimestamp = millis();
}
              
void commande_pin_mode() {
    char pin,mode;
    while (Serial.available()<2);
    pin = Serial.read(); // pin number
    mode = Serial.read(); // 0 = INPUT, 1 = OUTPUT
    pinMode(pin,mode);
}
              
void commande_digital_write() {
   char pin,output;
   while (Serial.available()<2);
   pin = Serial.read(); // pin number
   output = Serial.read(); // 0 = LOW, 1 = HIGH
   digitalWrite(pin,output);
}
              
void commande_digital_read() {
   char pin,input;
   while (Serial.available()<1);
   pin = Serial.read(); // pin number
   input = digitalRead(pin);
   Serial.write(input);
}
              
void commande_analog_write() {
   char pin,output;
   while (Serial.available()<2);
   pin = Serial.read(); // pin number
   output = Serial.read(); // PWM value between 0 and 255
   analogWrite(pin,output);
}
              
void commande_analog_read() {
   char pin;
   int value;
   while (Serial.available()<1);
   pin = Serial.read(); // pin number
   value = analogRead(pin);
   Serial.write((value>>8)&0xFF); // 8 bits de poids fort
   Serial.write(value & 0xFF); // 8 bits de poids faible
}

void commande_servo_attach(){
  char pin;
  int numeroServo;
  while (Serial.available()<2);
  numeroServo = Serial.read();
  pin = Serial.read();
  if(numeroServo==1) monservo.attach(pin);
  if(numeroServo==2) monservo2.attach(pin);
}

void commande_servo_write(){
  char pin;
  int numeroServo, value=0;
  while (Serial.available()<1);
  numeroServo = Serial.read();
  while (Serial.available()<1);
  value = Serial.read();
  if(numeroServo==1) monservo.write(value);
  if(numeroServo==2) monservo2.write(value);
}

              
