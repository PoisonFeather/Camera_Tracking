#include <Servo.h>
Servo servo;

int servo_count = 90;
String input;

void setup() {
  // put your setup code here, to run once:
  //Sservo.attach(9);
  Serial.begin(9600);
  servo.attach(9);
  bool nu_mai_vrem_calibrare = true;
  
  if (nu_mai_vrem_calibrare == false) {

    for (int i = 0; i < 180; i++) {
      servo.write(i);
      //  Serial.print(" " + i);
      delay(15);
    }
    for (int i = 180; i > 0; i--) {
      servo.write(i);
      delay(15);
    }
    //Serial.println("Done calibrating...");
    for (int i = 0; i <= 90; i++) {
      servo.write(i);

      Serial.print(".");
      delay(25);
    }
  }
  servo.write(90);
  //Serial.println();
}

void loop() {
  //digitalWrite(9,LOW);
  // put your main code here, to run repeatedly
  if(servo.attached() != true){
      servo.attach(9);
    }
  if (Serial.available()>0) {
      delay(25);
      input=Serial.readStringUntil('\n');
      //input=input.toInt();
      if(input == "+" ){
        servo_count+=5;
        servo.write(servo_count);
        if(servo_count >180) servo_count=180;
      }
      if(input == "-"){
          servo_count-=5;
          servo.write(servo_count);
          if(servo_count<10) servo_count=10;
        }
    Serial.flush();
  }else{
    servo.detach();
    }
}
