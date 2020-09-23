#include <Servo.h>

Servo servo;
int led = 2;
int servo_count = 90;
String input;

void setup() {
  // put your setup code here, to run once:
  //Sservo.attach(9);
  Serial.begin(9600);
  servo.attach(9);
  // calibrare
  //Serial.println("calibrating...");


  for (int i = 0; i < 180; i++) {
    servo.write(i);
    //  Serial.print(" " + i);
    delay(10);
  }
  for (int i = 180; i > 0; i--) {
    servo.write(i);
    delay(10);
  }
  //Serial.println("Done calibrating...");
  for (int i = 0; i <= 90; i++) {
    servo.write(i);

    Serial.print(".");
    delay(5);
  }
  //Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly
  if (servo.attached() != true) {
    servo.attach(9);
  }
  if (Serial.available()) {
    //Serial.write(Serial.read());
     input = Serial.readString();
     int angle=input.toInt();
     Serial.print(input);
    if (angle == 1 ) {
      servo_count += 10;
      servo.write(servo_count);
      delay(30);
      servo.write(servo_count);
    }
    else {
      if (angle == 0 ) {
        servo_count -= 10;
        servo.write(servo_count);
        delay(30);
        servo.write(servo_count);
      }
    }
    //Serial.println("servo: "+ servo.read());
  }
}
