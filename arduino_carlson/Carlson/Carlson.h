// Carlson: Chute Deployment and Logging System
// Code by Benjamin Shanahan

#ifndef CARLSON
#define CARLSON

#include <SD.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#define SERIAL true                // instantiate serial connection
#define PRINT_SENSOR_VALUES true  // print MPU6050 sensor values to serial
#define PRINT_CHUTE_DEPLOY false   // indicate that chute was deployed
#define PRINT_LOOP_TIMER false     // print how long sampling loop is taking to complete

// MPU6050 Calibration Offsets
// Determined using CalibrateMPU6050 script
#define OFFSET_ACCEL_X 795
#define OFFSET_ACCEL_Y 175
#define OFFSET_ACCEL_Z 1606
#define OFFSET_GYRO_X  33
#define OFFSET_GYRO_Y  -6
#define OFFSET_GYRO_Z  23

// Hardware and processing definitions
#define N_ITERS_BEFORE_FLUSH      20     // # of loops before data is flushed
#define MICROPHONE_PIN            A0     // mic input pin on arduino
#define BLUE_LED_PIN              8      // blue led
#define GREEN_LED_PIN             9      // green led
#define ERROR_BLINK_DELAY         200    // blink delay in ms if we have an error
#define DETONATION_RELAY_PIN      5      // chute detonation relay
#define CHIP_SELECT_PIN           10     // SD card logger chip select (CS) pin
#define BAUD_RATE                 9600   // serial port baud rate
#define N_ITERS_MIC_SAMPLE        40     // # of iters to sample mic over
#define MAXIMUM_ANALOG_IN_VALUE   1024   // maximum analog input value

// Carlson bit-mapped flag definitions
#define FLAG_DEFAULT              0  // default (boot/takeoff/flying)
#define FLAG_CARLSON_CHUTE_DEPLOY 1  // Carlson deployed chute
#define FLAG_MANUAL_CHUTE_DEPLOY  2  // manual RC deployed chute

// MPU6050-specific variables
MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;  // raw accel / gyro values
int16_t temperature;
double  microphone;
int     flightFlag;

// Computed variables
uint32_t loopTimer;  // check computation time
uint32_t timestamp;  // timestamp of sample data point
uint32_t time, timePrev;
double timeStep;
float micDiff, micVolts;
double asx, asy, asz, gsx, gsy, gsz;  // scaled
double arx, ary, arz, grx, gry, grz, rx, ry, rz;  // rotation

// Additional helper variables
int     m            = 0;
int16_t sample       = 0;
int     minMicSample = 1024;
int     maxMicSample = 0;
int32_t sumax = 0, sumay = 0, sumaz = 0, sumgx = 0, sumgy = 0, sumgz = 0;

// Counters and booleans
bool firstRun     = true;   // is this the first loop of the code?
int flushCounter  = 0;      // number of loops after last flush
double accelScale = 1.0/16384;  // from datasheet
double gyroScale  = 1.0/131;    // from datasheet

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
void    setup();
void    loop();
int     writeToLog(uint32_t ts,
    float ax, float ay, float az, 
    float gx, float gy, float gz, 
    float temp, float mic);
void    setCalibratedOffsets();
bool    initializeSDLogging();
void    printSensorValues();
double  getMicrophoneAmplitude();
void    checkForChuteDeploy();
void    blinkError();

#endif  // CARLSON