#ifndef ANOMALY_DETECTOR_H
#define ANOMALY_DETECTOR_H

struct SensorSample {
    float vibration;
    float temperature;
};

class AnomalyDetector {
public:
    static bool is_anomaly(const SensorSample& data) {
        return data.vibration > 10.0f || data.temperature > 90.0f;
    }
};

#endif  // ANOMALY_DETECTOR_H
