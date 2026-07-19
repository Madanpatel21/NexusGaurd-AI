#include <gtest/gtest.h>
#include "protocol_mqtt.h"

TEST(MqttProtocolTest, ConnectSetsState) {
    MQTTClient client;
    EXPECT_FALSE(client.is_connected());
    client.connect("mqtt://cloud:1883");
    EXPECT_TRUE(client.is_connected());
}

TEST(MqttProtocolTest, PublishIncrementsCounter) {
    MQTTClient client;
    client.connect("mqtt://cloud:1883");
    int before = client.publish_count();
    const char* payload = "anomaly";
    client.publish("anomaly", payload);
    EXPECT_EQ(client.publish_count(), before + 1);
}
