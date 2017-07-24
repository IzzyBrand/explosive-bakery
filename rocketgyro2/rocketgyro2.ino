#include <SD.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#define N_ITERS_BEFORE_FLUSH 20  // number of loops before data is flushed to file (higher = faster, but more risk of data loss)

MPU6050 accelgyro;
const int micPin = A0;

int16_t ax, ay, az, gx, gy, gz;
int16_t temperature;
int16_t microphone;

double timeStep, time, timePrev;
double arx, ary, arz, grx, gry, grz, gsx, gsy, gsz, rx, ry, rz;

bool firstRun = true;  // is this the first loop of the code?
int flushCounter = 0;  // keep track of how many loops we've been through before we want to flush to file
double gyroScale = 131;

String incrementFileName = "counter.txt";  // the name of the file that stores the log number
String logFileName = "noCounter.txt"; // this is the default filename to write to if we don't get a log number
int logNumber = 0;  // string to store the number we read from counterFile

int chipSelect = 10;

File incrementFile;
File logFile;

void setup() {

  Wire.begin();
  Serial.begin(9600);
  time = millis();

  // open counterFile and read in the number
  if (!SD.begin(chipSelect)) {
    Serial.println("Card initialization failed!");
    // TODO: make this error more aggressive
    return;
  }
  incrementFile = SD.open(incrementFileName);

  if (incrementFile) {
    // Serial.println("incrementFile initialized");
    logNumber = incrementFile.parseInt();
    incrementFile.close();
    SD.remove(incrementFileName);
  }
  // open the counterFile as WRITE and write the next number
  incrementFile = SD.open(incrementFileName, FILE_WRITE);
  if (incrementFile) {
    incrementFile.print(logNumber + 1);
    incrementFile.close();
  }
  // turn the logNumber into a fileName and open it to log to
  if (logNumber > 0)
    logFileName = "log_" + String(logNumber) + ".txt";

  // initialize arduino hardware
  pinMode(micPin, INPUT);
  accelgyro.initialize();

  // open logfile
  logFile = SD.open(logFileName, FILE_WRITE);
  
  delay(1);

}

void loop() {
  /**
    Important TODO:
      - take multiple readings per loop step and average them to filter out noise
        + this includes accelerometer / gyro / temperature / microphone
      - determine what to do about nan accelerometer values
      - re-enable filtering to get better angle measurements
  */

  // set up time for integration
  timePrev = time;
  time = millis();
  timeStep = (time - timePrev) / 1000; // time-step in s

  // collect readings
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  temperature = accelgyro.getTemperature();
  microphone = analogRead(micPin);

  // apply gyro scale from datasheet
  gsx = gx / gyroScale;
  gsy = gy / gyroScale;
  gsz = gz / gyroScale;

  // calculate accelerometer angles
  arx = (180 / 3.141592) * atan(ax / sqrt(sq(ay) + sq(az))); 
  ary = (180 / 3.141592) * atan(ay / sqrt(sq(ax) + sq(az)));
  arz = (180 / 3.141592) * atan(sqrt(sq(ay) + sq(ax)) / az);

  // set initial values equal to accel values
  if (firstRun) {
    if (isnan(arx))
      grx = 0;
    else
      grx = arx;
    if (isnan(ary))
      gry = 0;
    else
      gry = ary;
    if (isnan(arz))
      grz = 0;
    else
      grz = arz;
    firstRun = false;  // never again!
  } else {  // integrate to find the gyro angle
    grx = grx + (timeStep * gsx);
    gry = gry + (timeStep * gsy);
    grz = grz + (timeStep * gsz);
  }  

  // apply filter
  rx = (0.96 * arx) + (0.04 * grx);
  ry = (0.96 * ary) + (0.04 * gry);
  rz = (0.96 * arz) + (0.04 * grz);

  // print result
  //  Serial.print(i);   Serial.print("\t");
  //  Serial.print(timePrev);   Serial.print("\t");
  //  Serial.print(time);   Serial.print("\t");
  //  Serial.print(timeStep, 5);   Serial.print("\t\t");
  //  Serial.print(ax);   Serial.print("\t");
  //  Serial.print(ay);   Serial.print("\t");
  //  Serial.print(az);   Serial.print("\t\t");
  //  Serial.print(gx);   Serial.print("\t");
  //  Serial.print(gy);   Serial.print("\t");
  //  Serial.print(gz);   Serial.print("\t\t");
  //  Serial.print(temperature); Serial.print("\t");
  //  Serial.print(arx);   Serial.print("\t");
  //  Serial.print(ary);   Serial.print("\t");
  //  Serial.print(arz);   Serial.print("\t\t");
  //  Serial.print(grx);   Serial.print("\t");
  //  Serial.print(gry);   Serial.print("\t");
  //  Serial.print(grz);   Serial.print("\t");
  //  Serial.print(rx);   Serial.print("\t");
  //  Serial.print(ry);   Serial.print("\t");
  //  Serial.print(rz);
  //  Serial.print(gsx); Serial.print("\t");
  //  Serial.print(gsy); Serial.print("\t");
  //  Serial.print(gsz); Serial.print("\t");
  //  Serial.println();

  writeToLog(arx, ary, arz,  // rot from acceleration
            grx, gry, grz,  // rot from gyro
            microphone, temperature);

  delay(1);

}

// Write data to logfile on SD card
int writeToLog(float ax, float ay, float az, float gx, float gy, float gz, int16_t mic, int16_t temp) {
  String strLine = String(ax) + ",\t" + String(ay) + ",\t" + String(az) + ",\t" + 
                   String(gx) + ",\t" + String(gy) + ",\t" + String(gz) + ",\t" + 
                   String(mic) + ",\t" + String(temp);
  Serial.println(strLine);
  logFile.println(strLine);
  if (flushCounter == N_ITERS_BEFORE_FLUSH) {
    logFile.flush();
    flushCounter = 0;
  }
  flushCounter += 1;
}

/*
 *  +/- 250 degrees/s  (default)
 *  +/- 500 degrees/s  
 *  +/- 1000 degrees/s 
 *  +/- 2000 degrees/s 
 */
float raw_to_degrees(long raw, int scale) {
  return float(raw) / 32768.0 * float(scale);
}

/*
 *  +/- 2g  (default)
 *  +/- 4g 
 *  +/- 8g  
 *  +/- 16g 
 */
float raw_to_mss(long raw, int scale) {
  return float(raw) / 32768.0 * float(scale) * 9.81;
}
