// edge/firmware/src/main.cpp
#include <iostream>
#include "sensor_driver.h"
#include "protocol_mqtt.h"
#include "actuator_control.h"

int main() {
    SensorDriver::init();
    MQTTClient::connect("mqtt://cloud:1883");
    
    while (true) {
        auto data = SensorDriver::read();
        if (AnomalyDetector::is_anomaly(data)) {
            ActuatorControl::adjust_parameters(data);
            MQTTClient::publish("anomaly", data);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}
