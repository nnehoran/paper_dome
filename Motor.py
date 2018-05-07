import maestro

class Motor:
    """docstring for Motor"""

    MIN_PULSE = 496*4
    MAX_PULSE= 2448*4
    MAX_ANGLE_RANGE = 170

    MAX_SPEED = 0
    MAX_ACCEL = 15

    def __init__(self, controller, channel, min_angle = -MAX_ANGLE_RANGE/2, max_angle = MAX_ANGLE_RANGE/2, offset_angle = 0):
        self.controller = controller
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.offset_angle = offset_angle
        
        self.controller.setRange(self.channel, self.get_pulse_width(self.min_angle), self.get_pulse_width(self.max_angle))

    def get_min(self):
        return self.min_angle

    def get_max(self):
        return self.max_angle

    def get_pulse_width(self, angle):
        pulse_range = self.MAX_PULSE - self.MIN_PULSE
        center_pulse = (self.MAX_PULSE + self.MIN_PULSE)/2
        comp_angle = angle + self.offset_angle
        return int(center_pulse + pulse_range*(comp_angle)/self.MAX_ANGLE_RANGE)

    def get_position(self):
        return self.controller.getPosition(self.channel)

    def is_moving(self):
        return self.controller.isMoving(self.channel)

    def set_target(self, angle, speed = MAX_SPEED, accel = MAX_ACCEL):
        self.set_speed(speed)
        self.set_accel(accel)
        self.controller.setTarget(self.channel, self.get_pulse_width(angle))

    def set_speed(self, speed):
        self.controller.setSpeed(self.channel, speed)

    def set_accel(self, accel):
        self.controller.setAccel(self.channel, accel)
        
