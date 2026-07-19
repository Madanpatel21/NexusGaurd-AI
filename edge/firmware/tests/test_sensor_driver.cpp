#include <gtest/gtest.h>
#include "sensor_driver.h"

TEST(SensorDriverTest, ReadVibrationReturnsValue) {
    EXPECT_FLOAT_EQ(SensorDriver::read_vibration(), 4.5f);
}

TEST(SensorDriverTest, ReadReturnsCombinedData) {
    auto data = SensorDriver::read();
    EXPECT_FLOAT_EQ(data.vibration, 4.5f);
    EXPECT_FLOAT_EQ(data.temperature, 60.0f);
}
