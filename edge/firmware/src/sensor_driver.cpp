// edge/firmware/src/sensor_driver.cpp
#include "sensor_driver.h"

float SensorDriver::read_vibration() {
    // I2C read from accelerometer
    return i2c_read(0x68, REG_VIBRATION);
}
