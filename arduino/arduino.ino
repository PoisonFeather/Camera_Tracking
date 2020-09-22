#include <Servo.h>

int input;
Servo servo;
int led = 2;
void setup() {
  // put your setup code here, to run once:
  //Sservo.attach(9);
  Serial.begin(9600);
  servo.attach(9);
  // calibrare
  Serial.println("calibrating...");
  for(int i=0; i<180;i++){
      servo.write(i);
      Serial.print(" " + i);
      delay(10);
    }
  for(int i=180; i>0;i--){
      servo.write(i);
      delay(10);
    }
  Serial.println("Done calibrating...");
  for(int i=0;i<=90;i++){
      servo.write(i);
      
      Serial.print(".");
      delay(5);
    }
   Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
     if(servo.attached()!= true) servo.attach(9);
     
      input = Serial.parseInt();
      if( input >=10){
      servo.write(int(input));
      delay(10);
      servo.write(int(input));
      Serial.println(input);
      }
    }
  else{
      servo.detach();
    }
}
