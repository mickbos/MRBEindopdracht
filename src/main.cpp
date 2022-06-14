/* This example shows how to use continuous mode to take
range measurements with the VL53L0X. It is based on
vl53l0x_ContinuousRanging_Example.c from the VL53L0X API.
The range readings are in units of mm. */

#include <Arduino.h>
#include <Wire.h>

#include <Servo.h>

#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

VL53L0X_RangingMeasurementData_t measure;

Servo myservo;

const int arraySize = 3;
int measurementArray[arraySize] = {};
int arrayCounter = 0;
int tmp;

int movingAverage(){
	tmp = 0;
	lox.rangingTest(&measure, false);
	measurementArray[arrayCounter] = measure.RangeMilliMeter;
	arrayCounter += 1;
	if(arrayCounter >= arraySize){
		arrayCounter = 0;
	}
	for(int i = 0; i < arraySize; i++){
		tmp += measurementArray[i];
	}
	return tmp/arraySize;
}

float error = 0.0;
float error_sum = 0.0;
float error_div = 0.0;
float error_prev = 0.0;

float Kp = 0.3;
float Kd = 0.9;

float PID(int setpoint){
	error = setpoint - movingAverage();
	Serial.print("Error: ");
	Serial.println(error);
	error_div = error - error_prev;
	Serial.print("Error_div: ");
	Serial.println(error_div);
	int stuuractie = error * Kp + error_div * Kd;
	Serial.print("Stuuractie: ");
	Serial.println(stuuractie);
	error_prev = error;
	return stuuractie;
};

void setup() {
	Serial.begin(115200);
	myservo.attach(9);
	myservo.write(90);
	analogReadResolution(10);
	// wait until serial port opens for native USB devices
	while (! Serial) {
		delay(1);
	}

	Serial.println("Adafruit VL53L0X test");
	if (!lox.begin()) {
		Serial.println(F("Failed to boot VL53L0X"));
		while(1);
	}
	// power 
	Serial.println(F("VL53L0X API Simple Ranging example\n\n")); 

}

void loop() {
	int potPosition = map(analogRead(10), 0, 1023, 100, 400);
	int actie = PID(potPosition);

	// Serial.println(actie);
	myservo.write(actie + 70);
	delay(30);
};