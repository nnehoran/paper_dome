import Motor

class Trigger(Motor):
    """docstring for Trigger"""
    def __init__(self, controller, channel, neutral_angle = 0, travel = Motor.MAX_ANGLE_RANGE/2):
        super(Trigger, self).__init__(controller, channel, offset_angle = neutral_angle)
        self.travel = travel

    def set_on(self):
        self.set_target(self.travel)

    def set_off(self):
        self.set_target(0)
