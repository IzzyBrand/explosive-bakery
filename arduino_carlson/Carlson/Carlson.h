// Carlson: Chute Deployment and Logging System
// Code by Benjamin Shanahan

#ifndef CARLSON
#define CARLSON

#include <SD.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// MPU6050 Calibration Offsets
// Determined using CalibrateMPU6050 script
#define OFFSET_ACCEL_X 795
#define OFFSET_ACCEL_Y 175
#define OFFSET_ACCEL_Z 1606
#define OFFSET_GYRO_X  33
#define OFFSET_GYRO_Y  -6
#define OFFSET_GYRO_Z  23

// Hardware and processing definitions
#define N_ITERS_BEFORE_FLUSH   20     // number of loops before data is flushed
#define MICROPHONE_PIN         A0     // microphone input pin on arduino
#define CHIP_SELECT_PIN        10     // SD card logger chip select (CS) pin
#define SERIAL_CONNECTION      true   // instantiate serial connection and print
#define BAUD_RATE              9600   // serial port baud rate

// MPU6050-specific variables
MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;  // store values from accelerometer and gyroscope
int16_t temperature;
int16_t microphone;

// Computed timing and rotation variables
double timeStep, time, timePrev;
double arx, ary, arz, grx, gry, grz, gsx, gsy, gsz, rx, ry, rz;

// Counters and booleans
bool firstRun = true;    // is this the first loop of the code?
int flushCounter = 0;    // number of loops after last flush
double gyroScale = 131;

// Saving and incrementing data logfiles
String incrementFileName = "counter.txt";  // incremental data file name
String logFileName = "noCounter.txt";  // default filename 
File incrementFile;
File logFile;
int logNumber = 0;  // string to store the number we read from counterFile

// Functions
void setup();
void loop();
int writeToLog(float ax, float ay, float az, float gx, float gy, float gz, int16_t mic, int16_t temp);
// float raw_to_degrees(long raw, int scale);
// float raw_to_mss(long raw, int scale);

#endif  // CARLSON