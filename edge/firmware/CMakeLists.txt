cmake_minimum_required(VERSION 3.10)
project(NexusGuardFirmware)
set(CMAKE_CXX_STANDARD 17)

# Main firmware binary
add_executable(firmware
    src/main.cpp
    src/sensor_driver.cpp
    src/protocol_mqtt.cpp
    src/actuator_control.cpp
)
target_include_directories(firmware PRIVATE include)
target_link_libraries(firmware rt pthread)

# Unit tests (Google Test)
enable_testing()

find_package(GTest REQUIRED)
include(GoogleTest)

add_executable(firmware_tests
    tests/test_sensor_driver.cpp
    tests/test_mqtt_protocol.cpp
    tests/test_actuator_control.cpp
    tests/test_anomaly_detection.cpp
    tests/test_firmware_main_loop.cpp
    src/sensor_driver.cpp
    src/protocol_mqtt.cpp
    src/actuator_control.cpp
)
target_include_directories(firmware_tests PRIVATE include)
target_link_libraries(firmware_tests GTest::gtest GTest::gtest_main rt pthread)

add_test(NAME test_sensor_driver COMMAND firmware_tests --gtest_filter=SensorDriverTest.*)
add_test(NAME test_mqtt_protocol COMMAND firmware_tests --gtest_filter=MqttProtocolTest.*)
add_test(NAME test_actuator_control COMMAND firmware_tests --gtest_filter=ActuatorControlTest.*)
add_test(NAME test_anomaly_detection COMMAND firmware_tests --gtest_filter=AnomalyDetectionTest.*)
add_test(NAME test_firmware_main_loop COMMAND firmware_tests --gtest_filter=FirmwareMainLoopTest.*)
