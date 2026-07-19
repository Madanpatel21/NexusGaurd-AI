#ifndef SENSOR_DRIVER_H
#define SENSOR_DRIVER_H

#include <cstdint>

// Mock I2C primitives (stand-ins for the real hardware i2c.h).
#define REG_VIBRATION 0x00
inline float i2c_read(uint8_t addr, uint8_t reg) {
    (void)addr;
    (void)reg;
    return 4.5f;  // deterministic value for tests
}

class SensorDriver {
public:
    static void init() {}
    static float read_vibration();
    static float read_temperature() { return 60.0f; }

    struct SensorData {
        float vibration;
        float temperature;
    };
    static SensorData read() {
        return SensorData{read_vibration(), read_temperature()};
    }
};

#endif  // SENSOR_DRIVER_H
