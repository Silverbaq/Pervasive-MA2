#include <CommunicationUtils.h>
#include <DebugUtils.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <FreeSixIMU.h>

#include <Wire.h>



int q[6]; //hold q values
int incomingByte = 0;   // for incoming serial data

// Set the FreeIMU object
FreeSixIMU my3IMU = FreeSixIMU();

void setup() {
  
 
  Serial.begin(9600);

  Wire.begin();

  delay(5);
  my3IMU.init();
  delay(5);

}

void loop(){
  
  my3IMU.getRawValues(q);

  String s = String(q[0]) + "," + String(q[1]) + "," + String(q[2]) + "," + String(q[3]) + "," + String(q[4]) + "," + String(q[5]);
  Serial.println(s);


  
  delay(500);
  

  
}
