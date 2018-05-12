from Motor import Motor

class Trigger(Motor):
    """docstring for Trigger"""
    def __init__(self, controller, channel, name = 'motor', neutral_pulse = 0, pulse_travel = 100):
        super(Trigger, self).__init__(controller, channel, name = name)
        self.neutral_pulse = neutral_pulse
        self.pulse_travel = pulse_travel

    def set_on(self):
        self.set_pulse_target(self.neutral_pulse + self.pulse_travel)

    def set_off(self):
        self.set_pulse_target(self.neutral_pulse)
