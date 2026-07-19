#ifndef PROTOCOL_MQTT_H
#define PROTOCOL_MQTT_H

#include <cstddef>
#include <cstring>
#include <string>

// Mock MQTT client (stand-in for mqtt_client.h).
struct mqtt_client_t {
    bool connected = false;
    std::string last_topic;
    std::string last_payload;
    int publish_count = 0;
};

inline void mqtt_client_init(mqtt_client_t* c) { c->connected = false; }
inline void mqtt_client_connect(mqtt_client_t* c, const char* broker, int port, void* opts) {
    (void)broker; (void)port; (void)opts;
    c->connected = true;
}
inline void mqtt_publish(mqtt_client_t* c, const char* topic, const void* data, size_t len, int qos) {
    (void)qos;
    c->last_topic = topic;
    c->last_payload.assign(static_cast<const char*>(data), len);
    c->publish_count++;
}

class MQTTClient {
public:
    mqtt_client_t client;
    void connect(const char* broker);
    void publish(const char* topic, const void* data);
    bool is_connected() const { return client.connected; }
    int publish_count() const { return client.publish_count; }
};

#endif  // PROTOCOL_MQTT_H
