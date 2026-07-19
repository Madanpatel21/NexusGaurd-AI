#include "actuator_control.h"
#include <iostream>

bool ActuatorControl::last_adjusted = false;

void ActuatorControl::adjust_parameters(float vibration) {
    last_adjusted = false;
    if (vibration > 12.0) {
        std::cout << "Adjusting motor speed to reduce vibration..." << std::endl;
        // Write to hardware register
        last_adjusted = true;
    }
}
