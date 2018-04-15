
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
int ecart = 0;
long maxDist = log(PI+1);
long dist = 0;
long vitesse = 0;
long tps = 0;
long angle = 0;
long angleDep =0;
              
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
     if (commande==MAPPING){
        ecart = 0;
        for(int i=0; i<5; i++)
        {
          while (Serial.available()<1);
          ecart = ecart + Serial.read() * pow(10, 5-i) / 10;
        }
        ecart = 100;
        dist = map(ecart, 0, 240, 0, maxDist);
        vitesse = exp(dist) - 1;
        tps = (dist + vitesse)*1000;
        startTimestamp = millis();
        angleDep = angle;
     }
     else if (commande==SERVO_WRITE) commande_servo_write();
     else if (commande==SERVO_ATTACH) commande_servo_attach();
     
  }
  timePos = int((millis() - startTimestamp));
  angle = map(timePos, 0, tps, angleDep, angleDep + 40);
  monservo.write(angle);
}

void commande_mapping() {
    int duree = 0;
    for(int i=0; i<5; i++)
    {
      while (Serial.available()<1);
      duree = duree + Serial.read() * pow(10, 5-i) / 10;
    }
    startTimestamp = millis();
    timePos = 0;
    while(timePos < duree)
    {
      timePos = int((millis() - startTimestamp));
      long angle = map(timePos, 0, duree, 0, 180);
      monservo.write(angle);
    }
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

              
