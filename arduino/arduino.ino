#include <Servo.h>

Servo servo;

void setup() {
  // put your setup code here, to run once:
  servo.attach(9);
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
      int input = int(Serial.read());
      servo.write(input);                                
    }
  
}
