#include <gtest/gtest.h>
#include "actuator_control.h"

TEST(ActuatorControlTest, AdjustsWhenVibrationHigh) {
    ActuatorControl::last_adjusted = false;
    ActuatorControl::adjust_parameters(15.0f);
    EXPECT_TRUE(ActuatorControl::last_adjusted);
}

TEST(ActuatorControlTest, NoAdjustWhenVibrationLow) {
    ActuatorControl::last_adjusted = false;
    ActuatorControl::adjust_parameters(3.0f);
    EXPECT_FALSE(ActuatorControl::last_adjusted);
}
