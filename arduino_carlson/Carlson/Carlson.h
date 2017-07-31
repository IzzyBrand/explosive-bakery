// Carlson: Chute Deployment and Logging System
// Code by Benjamin Shanahan

#ifndef CARLSON
#define CARLSON

#include <SD.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#define SERIAL true               // instantiate serial connection
#define PRINT_SENSOR_VALUES true  // print MPU6050 sensor values to serial
#define PRINT_CHUTE_STATUS false  // output status of parachute

// MPU6050 Calibration Offsets
// Determined using CalibrateMPU6050 script
#define OFFSET_ACCEL_X 795
#define OFFSET_ACCEL_Y 175
#define OFFSET_ACCEL_Z 1606
#define OFFSET_GYRO_X  33
#define OFFSET_GYRO_Y  -6
#define OFFSET_GYRO_Z  23

// Hardware and processing definitions
#define N_SAMPLES_PER_MEASUREMENT 100    // how many measurement iters to avg
#define N_ITERS_BEFORE_FLUSH      20     // # of loops before data is flushed
#define MICROPHONE_PIN            A0     // mic input pin on arduino
#define CHIP_SELECT_PIN           10     // SD card logger chip select (CS) pin
#define BAUD_RATE                 9600   // serial port baud rate
#define MAXIMUM_ANALOG_IN_VALUE   1024   // maximum analog input value

// Chute deployment Z acceleration vector threshold
#define DEPLOY_IF_Z_ACCEL_LESS_THAN -0.9  // (G-force) (neg. bc inversion)
#define FALL_TIME_REQ_PRE_DEPLOY    3000  // (ms) min freefall time req. in 
                                          // less than -0.9G before chute is
                                          // deployed

// MPU6050-specific variables
MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;  // raw accel / gyro values
int16_t temperature;
int16_t microphone;

// Computed variables
double timeStep, time, timePrev;
double micDiff, micVolts, tempAvg;
double asx, asy, asz, gsx, gsy, gsz;  // scaled
double arx, ary, arz, grx, gry, grz, rx, ry, rz;  // rotation

// Sum variables to help compute sample averages
int32_t sumTemperature = 0;
int     minMicSample   = 1024;
int     maxMicSample   = 0;
int32_t sumax = 0, sumay = 0, sumaz = 0, sumgx = 0, sumgy = 0, sumgz = 0;

// Counters and booleans
bool firstRun     = true;   // is this the first loop of the code?
int flushCounter  = 0;      // number of loops after last flush
double gyroScale  = 131;    // from datasheet
double accelScale = 16384;  // from datasheet

// Chute deployment specific
bool deployChute     = false;  // should we deploy the parachute?
int fallCounter      = 0;      // a counter to make sure we don't reset timeStartFall
double timeStartFall = 0;      // when did the rocket start falling?

// Saving and incrementing data logfiles
int logNumber            = 0;  // stores number read from incrementFile
String incrementFileName = "counter.txt";    // incremental data file name
String logFileName       = "noCounter.txt";  // default filename 
File incrementFile;
File logFile;

// Functions
void setup();
void loop();
int writeToLog(float ax, float ay, float az, float gx, float gy, float gz, int16_t mic, int16_t temp);
void setCalibratedOffsets();
void initializeSDLogging();

#endif  // CARLSON