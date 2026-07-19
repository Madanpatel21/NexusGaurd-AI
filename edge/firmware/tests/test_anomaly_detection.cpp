#include <gtest/gtest.h>
#include "anomaly_detector.h"

TEST(AnomalyDetectionTest, NormalReadingNotAnomaly) {
    AnomalyDetector::SensorData d{4.5f, 60.0f};
    EXPECT_FALSE(AnomalyDetector::is_anomaly(d));
}

TEST(AnomalyDetectionTest, HighVibrationIsAnomaly) {
    AnomalyDetector::SensorData d{12.0f, 60.0f};
    EXPECT_TRUE(AnomalyDetector::is_anomaly(d));
}

TEST(AnomalyDetectionTest, HighTemperatureIsAnomaly) {
    AnomalyDetector::SensorData d{4.5f, 95.0f};
    EXPECT_TRUE(AnomalyDetector::is_anomaly(d));
}
