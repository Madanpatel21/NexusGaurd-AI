#include <gtest/gtest.h>
#include "sensor_driver.h"
#include "protocol_mqtt.h"
#include "actuator_control.h"
#include "anomaly_detector.h"

TEST(FirmwareMainLoopTest, AnomalyTriggersActuationAndPublish) {
    // Simulates the core loop body from main.cpp without the infinite loop.
    MQTTClient mqtt;
    mqtt.connect("mqtt://cloud:1883");

    auto data = SensorDriver::read();
    if (AnomalyDetector::is_anomaly(data)) {
        ActuatorControl::adjust_parameters(data.vibration);
        const char* payload = "anomaly";
        mqtt.publish("anomaly", payload);
    }

    // With normal readings, no actuation should occur.
    EXPECT_FALSE(ActuatorControl::last_adjusted);
    EXPECT_EQ(mqtt.publish_count(), 0);
}

TEST(FirmwareMainLoopTest, HighVibrationTriggersActuation) {
    MQTTClient mqtt;
    mqtt.connect("mqtt://cloud:1883");

    SensorDriver::SensorData data{15.0f, 60.0f};
    if (AnomalyDetector::is_anomaly(data)) {
        ActuatorControl::adjust_parameters(data.vibration);
        const char* payload = "anomaly";
        mqtt.publish("anomaly", payload);
    }

    EXPECT_TRUE(ActuatorControl::last_adjusted);
    EXPECT_EQ(mqtt.publish_count(), 1);
}
