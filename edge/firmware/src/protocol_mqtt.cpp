// edge/firmware/src/protocol_mqtt.cpp
#include "protocol_mqtt.h"
#include <cstring>

void MQTTClient::connect(const char* broker) {
    mqtt_client_init(&client);
    mqtt_client_connect(&client, broker, 1883, NULL);
}

void MQTTClient::publish(const char* topic, const void* data) {
    mqtt_publish(&client, topic, data, sizeof(data), 0);
}
