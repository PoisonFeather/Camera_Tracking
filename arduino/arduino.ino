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
    delay(25);
  }
  for (int i = 180; i > 0; i--) {
    servo.write(i);
    delay(25);
  }
  //Serial.println("Done calibrating...");
  for (int i = 0; i <= 90; i++) {
    servo.write(i);

    Serial.print(".");
    delay(25);
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
    //b'\x02'
    input.replace("b","");
    input.replace("'","");
    input.replace("x0","");
    input.replace("\\","");
    input.replace(" ","");
    Serial.print("input: " + input);
    
    int angle = input.toInt();
    int len = 0;
    //len of angle
    int aux = angle;
    while (aux > 0) {
      len++;
      aux = aux / 10;
    }
    Serial.print("len: " + len);
    int arr[len];
    for (int i = 0; i < len; i++) {
      arr[i] = angle % 10;
      angle = angle / 10;
      if (angle == 0) i = len;
    }

    for (int j = 0; j < len; j++) {
      Serial.println(arr[j]);
    }
    Serial.print(input);
    for (int x = 0; x < len; x++) {
      Serial.print("arr: " + arr[x]);
      if (arr[x] == '1' ) {
       
        servo_count += 10;
        servo.write(servo_count);
        delay(500);
        if ( servo_count >= 180) {
          servo_count = 180;
        }
      }
      if (arr[x] == '2' ) {
        servo_count -= 10;
        servo.write(servo_count);
        delay(500);
        if (servo_count <= 10) {
          servo_count = 10;
        }
      }
    }
  } else {
    servo.detach();
  }
  //Serial.println("servo: "+ servo.read());
}
