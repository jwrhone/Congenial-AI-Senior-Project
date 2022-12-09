/*
 File/Sketch Name: SoundLocationFinder

 Version No.: v1.0 Created 8 September, 2019
 
 Original Author: Clyde A. Lettsome, PhD, PE, MEM
 
 Description:  This code/sketch makes finding the general direction of sound easy. This code/sketch is for a sound location finder using two microphone sensors
 in conjunction with an Arduino Uno. The code/sketch polls two microphone sensors in a sound location finder circuit. If sound is detected in one microphone sensor and not the
 other, the Arduino request a stepper motor in the circuit to turn the sound detection board in the direction of the sound. If the sound is detected in both microphones or no
 sound is detected, the circuit does nothing and continues to poll the microphone sensors.

 License: This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License (GPL) version 3, or any later
 version of your choice, as published by the Free Software Foundation.

 Notes: Copyright (c) 2019 by C. A. Lettsome Services, LLC
 For more information visit https://clydelettsome.com/blog/2019/09/08/my-weekend-project-sound-location-finder/

 */
#include <Servo.h>
Servo myservo;
const int stepsPerRevolution = 400;  // change this to fit the number of steps per revolution for your motor
const int numberOfSteps = stepsPerRevolution/8; //45 degree turns
const int rightSensorPin=8;
const int leftSensorPin=7;
boolean rightVal = 0;
boolean leftVal = 0;
int pos = 90;
int jump = 7;
int turndelay = 150;
int nextpos = pos + jump;
int prevpos = pos - jump;
String num = "8";

void setup()
{
  pinMode(leftSensorPin, INPUT); //Make pin 8 an input pin.
  pinMode(rightSensorPin, INPUT); //Make pin 7 an input pin.
  myservo.attach(9);

  Serial.begin (9600); // initialize the serial port:
  
}
  
void loop (){
if (Serial.available() > 0) {
  num = Serial.readStringUntil('\n');
  
}
Serial.print("Number received from Pi: ");
Serial.println(num);
while (num == "6"){

{
  //poll inputs for signal
  rightVal =digitalRead(rightSensorPin);
  leftVal =digitalRead(leftSensorPin);
  
  // when the sensor detects a signal above the threshold value set on sensor, turn finder to the direction of sound
  if (leftVal==LOW && rightVal==HIGH)
  {
    Serial.println("Turning Right");
    
    //turn finder in the direction of the sound
    for (int i = 0; i < jump; i++){
      pos = pos - i;
      myservo.write(pos);
      delay(40);
    }
    {
      //create pulse to turn motor one step at a time
     
    }
    delayMicroseconds(100000);
    delay(turndelay);
    rightVal = 0;
    leftVal = 0;
     if (Serial.available() > 0)
      num = Serial.readStringUntil('\n');
    if (num != "6")
      break;
  }
  else if (leftVal==HIGH && rightVal==LOW)
  {
    Serial.println("Turning Left");
      
    //turn finder in the direction of the sound
    for (int i = 0; i < jump; i++){
      pos = pos + i;
      myservo.write(pos);
      delay(40);
    }
    delayMicroseconds(100000);
    delay(turndelay);
    rightVal = 0;
    leftVal = 0;

     if (Serial.available() > 0)
      num = Serial.readStringUntil('\n');
    if (num != "6")
      break;
    
  }
  else 
  {
    //Do nothing
    rightVal = 0;
    leftVal = 0;

     if (Serial.available() > 0)
      num = Serial.readStringUntil('\n');
    if (num != "6")
      break;
    
  }
  if (pos < 0){
    pos = 0;
    for (int i = 0; i < 12; i++){
      pos = pos + i;
      myservo.write(pos);
      delay(40);
    }
  }
  if (pos > 180){
    pos = 180;
    for (int i = 0; i < 10; i++){
      pos = pos - i;
      myservo.write(pos);
      delay(40);
    }
  }
}
}
}
