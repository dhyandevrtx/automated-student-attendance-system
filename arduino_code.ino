#include <Servo.h>

Servo myservo;
int servoPin = 9;
int greenLedPin = 10;
int redLedPin = 11;
int yellowLedPin = 12;
int buzzerPin = 13;
int irSensor1 = 2;
int irSensor2 = 3;
int ldrPin = A0;

void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin);
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(yellowLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(irSensor1, INPUT);
  pinMode(irSensor2, INPUT);
  pinMode(ldrPin, INPUT);
}

void loop() {
  // Serial Input from Laptop
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == 'P') {
      digitalWrite(greenLedPin, HIGH);
      digitalWrite(redLedPin, LOW);
      digitalWrite(yellowLedPin, LOW);
      myservo.write(90);
      tone(buzzerPin, 1000); delay(500); noTone(buzzerPin);
    } else if (data == 'A') {
      digitalWrite(redLedPin, HIGH);
      digitalWrite(greenLedPin, LOW);
      digitalWrite(yellowLedPin, LOW);
      myservo.write(0);
      tone(buzzerPin, 500); delay(500); noTone(buzzerPin);
    } else if (data == 'L') {
        digitalWrite(yellowLedPin, HIGH);
        digitalWrite(redLedPin, LOW);
        digitalWrite(greenLedPin, LOW);
        myservo.write(90);
        tone(buzzerPin, 750); delay(500); noTone(buzzerPin);
    }
  }

  // Sensor Readings and Output to Laptop
  int ldrValue = analogRead(ldrPin);
  int irValue1 = digitalRead(irSensor1);
  int irValue2 = digitalRead(irSensor2);

  Serial.print("L"); Serial.println(ldrValue);
  Serial.print("I"); Serial.print(irValue1); Serial.print(","); Serial.println(irValue2);

  // Sensor Validation
  if (irValue1 == LOW || irValue2 == LOW) {
    if (ldrValue < 300) {
      tone(buzzerPin, 2000); delay(200); noTone(buzzerPin);
      Serial.println("F");
    } else {
      Serial.println("S");
    }
  }
  delay(100);
}
