#include <CommunicationUtils.h>
#include <DebugUtils.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <FreeSixIMU.h>

#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial mySerial(30,31); // RX, TX

int q[6]; //hold q values
int incomingByte = 0;   // for incoming serial data

// Set the FreeIMU object
FreeSixIMU my3IMU = FreeSixIMU();

void setup() {
  
  mySerial.begin(9600);
  Serial.begin(9600);

  Wire.begin();

  delay(5);
  my3IMU.init();
  delay(5);

  mySerial.println("Starting script");

}

void loop(){
  
  my3IMU.getRawValues(q);

  Serial.println(q[0]);
  mySerial.print(q[0]);
  mySerial.print(",");  
  mySerial.print(q[1]);  
  mySerial.print(",");  
  mySerial.print(q[2]);
  mySerial.print(",");  
  mySerial.print(q[3]);
  mySerial.print(",");  
  mySerial.print(q[4]);
  mySerial.print(",");  
  mySerial.println(q[5]);
  
  delay(500);
  
  
  if (mySerial.available())
  {
    incomingByte = mySerial.read();

    mySerial.println("HAHA");
    mySerial.println( incomingByte, OCT);
  }
  
  
}
