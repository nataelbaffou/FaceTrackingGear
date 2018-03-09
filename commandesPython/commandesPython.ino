
#define PIN_MODE 100
#define DIGITAL_WRITE 101
#define DIGITAL_READ 102
#define ANALOG_WRITE 103
#define ANALOG_READ 104
#define SERVO_WRITE 105
#define SERVO_READ 106
#define SERVO_ATTACH 107

#include <Servo.h>

Servo monservo;
Servo monservo2;
              
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
     if (commande==PIN_MODE) commande_pin_mode();
     else if (commande==DIGITAL_WRITE) commande_digital_write();
     else if (commande==DIGITAL_READ) commande_digital_read();
     else if (commande==ANALOG_WRITE) commande_analog_write();
     else if (commande==ANALOG_READ) commande_analog_read();
     else if (commande==SERVO_WRITE) commande_servo_write();
     else if (commande==SERVO_ATTACH) commande_servo_attach();
  }
  // autres actions à placer ici
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

              
