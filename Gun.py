import maestro
import Motor
import Trigger

class Gun:
    """docstring for Gun"""

    YAW_CHANNEL = 0
    PITCH_CHANNEL = 1
    TRIGGER_CHANNEL = 2

    def __init__(self):
        self.controller = maestro.Controller('COM3')
        self.yaw_motor = Motor.Motor(self.controller, self.YAW_CHANNEL)
        self.pitch_motor = Motor.Motor(self.controller, self.PITCH_CHANNEL, min_angle = -20, max_angle = 25)
        self.trigger = Trigger.Trigger(self.controller, self.TRIGGER_CHANNEL, neutral_angle = 0, travel = Motor.MAX_ANGLE_RANGE/2)

    def get_position(self):
        yaw = yaw_motor.get_position()
        pitch = yaw_motor.get_position()
        return (yaw, pitch)

    def is_moving(self):
        return not self.controller.getMovingState()

    def set_yaw(self, yaw, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.yaw_motor.set_target(yaw, speed, accel)

    def set_pitch(self, pitch, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.pitch_motor.set_target(pitch, speed, accel)

    def set_target(self, yaw, pitch, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.set_yaw(yaw, speed, accel)
        self.set_pitch(pitch, speed, accel)

    def fire(self):
        self.trigger.set_on()

    def stop_fire(self):
        self.trigger.set_off()

    def go_to_zero(self, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.stop_fire()
        self.set_target(self, 0, 0, speed, accel)
