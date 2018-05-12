import maestro
from Motor import Motor
from Trigger import Trigger

class Gun:
    """docstring for Gun"""

    YAW_CHANNEL = 0
    PITCH_CHANNEL = 1
    TRIGGER_CHANNEL = 2

    MAX_SPEED = 0
    MAX_ACCEL = 0

    def __init__(self):
        self.controller = maestro.Controller('COM3')
        self.yaw_motor = Motor(self.controller, self.YAW_CHANNEL, name = 'yaw',offset_angle = 10)
        self.pitch_motor = Motor(self.controller, self.PITCH_CHANNEL, name = 'pitch', max_angle = 20, offset_angle = 0)
        self.trigger = Trigger(self.controller, self.TRIGGER_CHANNEL, name = 'trigger', neutral_pulse = 1880*4, pulse_travel = 2080*4)

    def get_angles(self):
        yaw = self.yaw_motor.get_angle()
        pitch = self.yaw_motor.get_angle()
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
        print('%s, %s' %(yaw, pitch))

    def fire(self):
        self.trigger.set_on()

    def stop_fire(self):
        self.trigger.set_off()

    def go_to_zero(self, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.stop_fire()
        self.set_target(0, 0, speed, accel)
