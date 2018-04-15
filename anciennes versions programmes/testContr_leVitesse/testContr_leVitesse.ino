#include <Servo.h>

Servo monservo;

int pinVitesse=9;
int pinAngle=7;

void setup(){
    pinMode(pinVitesse,OUTPUT);
    monservo.attach(pinAngle);
}
void loop(){
    monservo.write(0);
    delay(2000);
    monservo.write(180);
    digitalWrite(pinVitesse,HIGH); //le moteur se lance
    delay(1000);
    digitalWrite(pinVitesse,LOW); //le moteur s'arrête
    delay(500);
    
}
