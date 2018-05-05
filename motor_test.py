import maestro
import MotorControl
import time

controller = MotorControl.MotorControl('COM3')

controller.set_pitch_range(offset = 0)

controller.go_to_zero(20)
time.sleep(3)
# controller.set_target(-90, 0, 20)
# time.sleep(3)
# controller.set_target(0, 40, 20)
# time.sleep(3)
# controller.set_target(90, 0, 20)
# time.sleep(3)
# controller.go_to_zero(20)
# time.sleep(3)
controller.set_trigger(True)
time.sleep(2)
controller.set_trigger(False)


controller.close()