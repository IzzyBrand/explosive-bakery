// Carlson: Chute Deployment and Logging System
// 
// Code by: Benjamin Shanahan & Isaiah Brand

#include "Carlson.h"

void setup()
{

    Wire.begin();
    Serial.begin(BAUD_RATE);
    time = millis();

    // open counterFile and read in the number
    if (!SD.begin(CHIP_SELECT_PIN))
    {
        Serial.println("Card initialization failed!");
        // TODO: make this error more aggressive
        return;
    }
    incrementFile = SD.open(incrementFileName);

    if (incrementFile)
    {
        // Serial.println("incrementFile initialized");
        logNumber = incrementFile.parseInt();
        incrementFile.close();
        SD.remove(incrementFileName);
    }
    // open the counterFile as WRITE and write the next number
    incrementFile = SD.open(incrementFileName, FILE_WRITE);
    if (incrementFile)
    {
        incrementFile.print(logNumber + 1);
        incrementFile.close();
    }
    // turn the logNumber into a fileName and open it to log to
    if (logNumber > 0)
        logFileName = "log_" + String(logNumber) + ".txt";

    // initialize arduino hardware
    pinMode(MICROPHONE_PIN, INPUT);
    accelgyro.initialize();

    // Set accel/gyro offsets
    accelgyro.setXAccelOffset(OFFSET_ACCEL_X);
    accelgyro.setYAccelOffset(OFFSET_ACCEL_Y);
    accelgyro.setZAccelOffset(OFFSET_ACCEL_Z);  
    accelgyro.setXGyroOffset(OFFSET_GYRO_X);
    accelgyro.setYGyroOffset(OFFSET_GYRO_Y);
    accelgyro.setZGyroOffset(OFFSET_GYRO_Z);

    // open logfile
    logFile = SD.open(logFileName, FILE_WRITE);

    delay(1);

}

void loop()
{
    /**
    Important TODO:
      - take multiple readings per loop step and average them to filter out 
        noise
        + this includes accelerometer / gyro / temperature / microphone
      - determine what to do about nan accelerometer values
      - re-enable filtering to get better angle measurements
    */

    // set up time for integration
    timePrev = time;
    time     = millis();
    timeStep = (time - timePrev) / 1000; // convert timestep to seconds

    // collect readings
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    temperature = accelgyro.getTemperature();
    microphone = analogRead(MICROPHONE_PIN);

    // apply gyro scale from datasheet
    gsx = gx / gyroScale;
    gsy = gy / gyroScale;
    gsz = gz / gyroScale;

    // calculate accelerometer angles
    // arx = (180 / 3.141592) * atan(ax / sqrt(sq(ay) + sq(az))); 
    // ary = (180 / 3.141592) * atan(ay / sqrt(sq(ax) + sq(az)));
    // arz = (180 / 3.141592) * atan(sqrt(sq(ay) + sq(ax)) / az);

    // integration of gyroscopic angular acceleration values
    if (!firstRun)
    {
        grx = grx + (timeStep * gsx);
        gry = gry + (timeStep * gsy);
        grz = grz + (timeStep * gsz);
    }

    // TODO: get this working... this rotational estimate should be more accurate than previous
    // apply filter
    // rx = (0.96 * arx) + (0.04 * grx);
    // ry = (0.96 * ary) + (0.04 * gry);
    // rz = (0.96 * arz) + (0.04 * grz);

    Serial.print(String(ax) + "\t");
    Serial.print(String(ay) + "\t");
    Serial.print(String(az) + "\t");
    Serial.print(String(grx) + "\t");
    Serial.print(String(gry) + "\t");
    Serial.print(String(grz) + "\t");
    Serial.println();

    // writeToLog(ax, ay, az,  // rot from acceleration
    //         grx, gry, grz,  // rot from gyro
    //         microphone, temperature);

    if (firstRun) firstRun = false;
    delay(1);

}

// Write data to logfile on SD card
int writeToLog(float ax, float ay, float az, float gx, float gy, float gz, int16_t mic, int16_t temp)
{
    String strLine = String(ax) + ",\t" + String(ay) + ",\t" + String(az) + ",\t" + 
                    String(gx) + ",\t" + String(gy) + ",\t" + String(gz) + ",\t" + 
                    String(mic) + ",\t" + String(temp);
    Serial.println(strLine);
    logFile.println(strLine);
    if (flushCounter == N_ITERS_BEFORE_FLUSH) {
        // to increase speed, we only flush to file once every N_ITERS_BEFORE_FLUSH loops
        logFile.flush();
        flushCounter = 0;
    }
    flushCounter += 1;
}

// /*
//  *  +/- 250 degrees/s  (default)
//  *  +/- 500 degrees/s  
//  *  +/- 1000 degrees/s 
//  *  +/- 2000 degrees/s 
//  */
// float raw_to_degrees(long raw, int scale)
// {
//     return float(raw) / 32768.0 * float(scale);
// }

// /*
//  *  +/- 2g  (default)
//  *  +/- 4g 
//  *  +/- 8g  
//  *  +/- 16g 
//  */
// float raw_to_mss(long raw, int scale)
// {
//     return float(raw) / 32768.0 * float(scale) * 9.81;
// }
