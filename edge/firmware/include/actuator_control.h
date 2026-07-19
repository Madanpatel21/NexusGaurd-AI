#ifndef ACTUATOR_CONTROL_H
#define ACTUATOR_CONTROL_H

class ActuatorControl {
public:
    static void adjust_parameters(float vibration);
    static bool last_adjusted;
};

#endif  // ACTUATOR_CONTROL_H
