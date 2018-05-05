import maestro

class MotorControl(maestro.Controller):
    """docstring for MotorControl"""

    YAW_CHANNEL = 0
    PITCH_CHANNEL = 1
    TRIGGER_CHANNEL = 2

    MIN_PULSE = 496*4
    MAX_PULSE= 2448*4
    MAX_ANGLE_RANGE = 170

    MAX_SPEED = 0
    MAX_ACCEL = 15

    def __init__(self, com_port, yaw_range = MAX_ANGLE_RANGE, pitch_range = 90):
        super(MotorControl, self).__init__(com_port)
        self.set_yaw_range(yaw_range)
        self.set_pitch_range(pitch_range)
        self.setAccel(self.YAW_CHANNEL, self.MAX_ACCEL)
        self.setAccel(self.PITCH_CHANNEL, self.MAX_ACCEL)
        self.set_trigger_range(1872*4, 2016*4)

    def get_pulse_width(self, angle):
        center_pulse = (self.MAX_PULSE + self.MIN_PULSE)/2
        pulse_range = self.MAX_PULSE - self.MIN_PULSE
        return int(center_pulse + angle*pulse_range/self.MAX_ANGLE_RANGE)

    def set_range(self, chan, range):
        min_pulse = self.get_pulse_width(-range/2)
        max_pulse = self.get_pulse_width(range/2)
        maestro.Controller.setRange(self, chan, min_pulse, max_pulse)

    def set_yaw_range(self, range = MAX_ANGLE_RANGE, offset = 0):
        self.yaw_range = range
        self.yaw_offset = offset
        self.set_range(self.YAW_CHANNEL, range)

    def set_pitch_range(self, range = 90, offset = 0):
        self.pitch_range = range
        self.pitch_offset = offset
        self.set_range(self.PITCH_CHANNEL, range)

    def set_trigger_range(self, min_pulse, max_pulse):
        self.fire_pulse = max_pulse
        self.no_fire_pulse = min_pulse
        maestro.Controller.setRange(self, self.TRIGGER_CHANNEL, min_pulse, max_pulse)

    def set_yaw(self, yaw, speed = MAX_SPEED, zero = 'center'):
        if zero == 'min':
            pulse_width = self.get_pulse_width(-yaw - self.yaw_offset + self.yaw_range/2)
        else:
            pulse_width = self.get_pulse_width(-yaw - self.yaw_offset)

        maestro.Controller.setSpeed(self, self.YAW_CHANNEL, speed)
        maestro.Controller.setTarget(self, self.YAW_CHANNEL, pulse_width)

    def set_pitch(self, pitch, speed = MAX_SPEED, zero = 'min'):
        if zero == 'min':
            pulse_width = self.get_pulse_width(-pitch - self.pitch_offset + self.pitch_range/2)
        else:
            pulse_width = self.get_pulse_width(-pitch - self.pitch_offset)

        maestro.Controller.setSpeed(self, self.PITCH_CHANNEL, speed)
        maestro.Controller.setTarget(self, self.PITCH_CHANNEL, pulse_width)

    def set_trigger(self, fire):
        if fire:
            pulse_width = self.fire_pulse
        else:
            pulse_width = self.no_fire_pulse

        maestro.Controller.setTarget(self, self.TRIGGER_CHANNEL, pulse_width)

    def set_target(self, yaw, pitch, speed = MAX_SPEED):
        self.set_yaw(yaw, speed)
        self.set_pitch(pitch, speed)

    def go_to_zero(self, speed = MAX_SPEED):
        self.set_trigger(False)
        self.set_target(0, 0, speed)