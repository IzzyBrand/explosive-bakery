// Calibrate MPU6050
// Code by Benjamin Shanahan

// Source:
// https://www.i2cdevlib.com/forums/topic/91-how-to-decide-gyro-and-accelerometer-offsett/?do=findComment&comment=257

// To Run:
//   1. Place MPU6050 (after wiring) on level surface
//   2. Upload code and run
//   3. Adjust offsets until all values are roughly zero (except accelZ, 
//      which should be +16384)
//   7. Fill in offsets in "Carlson.h" file

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// Offsets (negate all gyro and accel computed averages, except accelZ, 
// which should add to +16384 instead of 0)
#define OFFSET_ACCEL_X 795
#define OFFSET_ACCEL_Y 175
#define OFFSET_ACCEL_Z 1606
#define OFFSET_GYRO_X 33
#define OFFSET_GYRO_Y -6
#define OFFSET_GYRO_Z 23


MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;
int32_t axavg, ayavg, azavg, gxavg, gyavg, gzavg;

int n = 10;  // average over n readings

void setup()
{
    Wire.begin();
    Serial.begin(9600);
    accelgyro.initialize();

    // Set accel/gyro offsets
    accelgyro.setXAccelOffset(OFFSET_ACCEL_X);
    accelgyro.setYAccelOffset(OFFSET_ACCEL_Y);
    accelgyro.setZAccelOffset(OFFSET_ACCEL_Z);  
    accelgyro.setXGyroOffset(OFFSET_GYRO_X);
    accelgyro.setYGyroOffset(OFFSET_GYRO_Y);
    accelgyro.setZGyroOffset(OFFSET_GYRO_Z);
}

void loop()
{
    // clear variables
    axavg = 0;
    ayavg = 0;
    azavg = 0;
    gxavg = 0;
    gyavg = 0;
    gzavg = 0;

    // collect average readings
    for (int i = 0; i < n; ++i)
    {
        // accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        axavg += accelgyro.getAccelerationX();
        ayavg += accelgyro.getAccelerationY();
        azavg += accelgyro.getAccelerationZ();
        gxavg += accelgyro.getRotationX();
        gyavg += accelgyro.getRotationY();
        gzavg += accelgyro.getRotationZ();
        delay(1);
    }
    axavg = axavg / n;
    ayavg = ayavg / n;
    azavg = azavg / n;
    gxavg = gxavg / n;
    gyavg = gyavg / n;
    gzavg = gzavg / n;

    // print readings
    Serial.print(String(axavg) + "\t");
    Serial.print(String(ayavg) + "\t");
    Serial.print(String(azavg) + "\t");
    Serial.print(String(gxavg) + "\t");
    Serial.print(String(gyavg) + "\t");
    Serial.println(String(gzavg));
    
    // delay(50);
}