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
    }
  for(i=180; i>0;i--){
      servo.write(i);
    }
  Serial.println("Done calibrating...");
  servo.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
     if(servo.attached()!= true) servo.attach(9);
     
      input = Serial.parseInt();
      servo.write(input);
      delay(10);
      Serial.println(input);
    }
  else{
      servo.detach();
    }
}
