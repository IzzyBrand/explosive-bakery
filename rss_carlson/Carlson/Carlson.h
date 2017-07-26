// Rocket Survey System: Carlson
// Code by Benjamin Shanahan

#ifndef CARLSON
#define CARLSON


// Definitions

#define N_ITERS_BEFORE_FLUSH    20     // number of loops before data is flushed
#define MICROPHONE_PIN          A0     // microphone input pin on arduino
#define CHIP_SELECT_PIN         10     // SD card logger chip select (CS) pin
#define SERIAL_CONNECTION       true   // instantiate serial connection and print
#define BAUD_RATE               9600   // serial port baud rate


// Variables

MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;  // store values from accelerometer and gyroscope


// Functions

void setup();
void loop();


#endif  // CARLSON