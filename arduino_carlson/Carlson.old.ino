// Carlson: Chute Deployment and Logging System
// 
// This script will boot Carlson, lock nose-cone after successful
// initialization, record gyro / accel / temperature / microphone sensor
// readings during rocket flight, and deploy chute at altitude. 
//
// Chute deployment occurs after the Z accelerometer consistently measures
// less than -0.9g of downward force for n seconds.
//
// Code by: Benjamin Shanahan & Isaiah Brand

#include "Carlson.h"

void setup()
{

    if (SERIAL)
        Serial.begin(BAUD_RATE);
    Wire.begin();
    time = millis();

    // initialize SD card logging
    initializeSDLogging();

    // initialize arduino hardware
    pinMode(MICROPHONE_PIN, INPUT);
    pinMode(BLUE_LED_PIN, OUTPUT);
    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(RELAY_PIN, OUTPUT);
    accelgyro.initialize();
    setCalibratedOffsets();  // set MPU6050 offsets

    // open logfile
    logFile = SD.open(logFileName, FILE_WRITE);

    if (SERIAL)
        Serial.println("Carlson initialization successful.");

    delay(1);

}

void loop()
{

    for (int i = 0; i < N_SAMPLES_PER_MEASUREMENT; i++)
    {
        // collect readings from hardware
        accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        temperature = accelgyro.getTemperature();
        microphone  = analogRead(MICROPHONE_PIN);

        // sum sensor readings
        sumax += ax;
        sumay += ay;
        sumaz += az;
        sumgx += gx;
        sumgy += gy;
        sumgz += gz;
        sumTemperature += temperature;

        // if current microphone reading is greater than or less than
        // max or min, respectively, replace those values
        if (microphone < MAXIMUM_ANALOG_IN_VALUE)  // reject impossible samples
        {
            if (microphone > maxMicSample)
                maxMicSample = microphone;
            else if (microphone < minMicSample)
                minMicSample = microphone;
        }

    }

    // average and apply accelerometer scale from datasheet
    asx = (sumax / N_SAMPLES_PER_MEASUREMENT) / accelScale;
    asy = (sumay / N_SAMPLES_PER_MEASUREMENT) / accelScale;
    asz = (sumaz / N_SAMPLES_PER_MEASUREMENT) / accelScale;

    // average and apply gyro scale from datasheet
    gsx = (sumgx / N_SAMPLES_PER_MEASUREMENT) / gyroScale;
    gsy = (sumgy / N_SAMPLES_PER_MEASUREMENT) / gyroScale;
    gsz = (sumgz / N_SAMPLES_PER_MEASUREMENT) / gyroScale;

    // compute average temperature and microphone sample difference
    tempAvg  = double(sumTemperature) / double(N_SAMPLES_PER_MEASUREMENT);
    micDiff  = maxMicSample - minMicSample;
    micVolts = (micDiff * 5.0) / MAXIMUM_ANALOG_IN_VALUE;  // convert to volts

    // reset sums
    sumax = 0; sumay = 0; sumaz = 0;
    sumgx = 0; sumgy = 0; sumgz = 0;
    sumTemperature = 0;
    maxMicSample = 0;
    minMicSample = MAXIMUM_ANALOG_IN_VALUE;

    // determine timestep for integration
    timePrev = time;
    time     = millis();
    timeStep = (time - timePrev) / 1000; // convert timestep to seconds

    // integration of gyroscopic angular acceleration values
    if (!firstRun)
    {
        grx = grx + (timeStep * gsx);
        gry = gry + (timeStep * gsy);
        grz = grz + (timeStep * gsz);
    }

    if (SERIAL && PRINT_SENSOR_VALUES)
    {
        Serial.print("A:\t");
        Serial.print(String(asx) + "\t");
        Serial.print(String(asy) + "\t");
        Serial.print(String(asz) + "\t\t");
        Serial.print("G:\t");
        Serial.print(String(grx) + "\t");
        Serial.print(String(gry) + "\t");
        Serial.print(String(grz) + "\t\t");
        Serial.print("T:\t");
        Serial.print(String(tempAvg) + "\t");
        Serial.print("M:\t");
        Serial.print(String(micVolts) + "V");
        Serial.println();
    }

    // check if we should deploy parachute
    if (asz < DEPLOY_IF_Z_ACCEL_LESS_THAN)
    {
        if (SERIAL && PRINT_CHUTE_STATUS)
            Serial.println("Rocket is falling!");

        if (fallCounter == 0)
            timeStartFall = millis();
        
        if (millis() - timeStartFall > FALL_TIME_REQ_PRE_DEPLOY)
            deployChute = true;

        fallCounter++;
    }
    else
        fallCounter = 0;

    // logic to deploy the parachute
    if (deployChute)
    {
        if (SERIAL && PRINT_CHUTE_STATUS)
            Serial.println("Deploying parachute!");

        // TODO: add logic to turn servo motor and deploy parachute
    }

    writeToLog(asx, asy, asz,  // rot from acceleration
               grx, gry, grz,  // rot from gyro
               tempAvg, micVolts);

    if (firstRun) firstRun = false;

}

// Write data to logfile on SD card
int writeToLog(float ax, float ay, float az, 
               float gx, float gy, float gz, 
               float temp, float mic)
{

    String strLine = String(ax)+",\t" + String(ay)+",\t" + String(az)+",\t" + 
                     String(gx)+",\t" + String(gy)+",\t" + String(gz)+",\t" + 
                     String(temp)+",\t" + String(mic);

    logFile.println(strLine);  // log to file
    
    if (flushCounter == N_ITERS_BEFORE_FLUSH) {
        // to increase speed, we only flush to file once every N_ITERS_BEFORE_FLUSH loops
        logFile.flush();
        flushCounter = 0;
    }
    
    flushCounter += 1;

}

// Write offsets to MPU6050
void setCalibratedOffsets()
{

    accelgyro.setXAccelOffset(OFFSET_ACCEL_X);
    accelgyro.setYAccelOffset(OFFSET_ACCEL_Y);
    accelgyro.setZAccelOffset(OFFSET_ACCEL_Z);  
    accelgyro.setXGyroOffset(OFFSET_GYRO_X);
    accelgyro.setYGyroOffset(OFFSET_GYRO_Y);
    accelgyro.setZGyroOffset(OFFSET_GYRO_Z);

}

// Initialize SD card logging functionality
// Code by Isaiah Brand
//
// Opens "counter.txt" on SD card, reads the integer contained in the file,
// increments it, and writes the incremented number to the file. This number
// is then appended to the in-flight logfile generated by Carlson (i.e. 
// "LOG_4.txt"). Afterwards, "counter.txt" is closed, and the new logfile is
// opened and available for writing data.
void initializeSDLogging()
{

    // open counterFile and read in the number
    if (!SD.begin(CHIP_SELECT_PIN))
    {
        if (SERIAL)
            Serial.println("Card initialization failed!");

        // TODO: make this error more aggressive; fail to lock nose cone
        return;
    }
    incrementFile = SD.open(incrementFileName);

    if (incrementFile)
    {
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

}