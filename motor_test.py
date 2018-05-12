import maestro
# import MotorControl
import time
import Gun

# controller = MotorControl.MotorControl('COM3')

# controller.set_pitch_range(offset = 0)

# controller.go_to_zero(20)
# time.sleep(3)
# controller.set_target(-90, 0, 20)
# time.sleep(3)
# controller.set_target(0, 40, 20)
# time.sleep(3)
# controller.set_target(90, 0, 20)
# time.sleep(3)
# controller.go_to_zero(20)
# time.sleep(3)
# controller.set_trigger(True)
# time.sleep(2)
# controller.set_trigger(False)


# controller.close()

movement = 20

gun = Gun.Gun()
gun.go_to_zero(speed = 10)
time.sleep(2)
gun.set_target(0, movement, speed = 10)
time.sleep(2)
gun.set_target(0, -movement, speed = 10)
time.sleep(3)
gun.go_to_zero(speed = 10)
time.sleep(2)
gun.set_target(movement, 0, speed = 10)
time.sleep(2)
gun.set_target(-movement, 0, speed = 10)
time.sleep(3)
gun.go_to_zero(speed = 10)
time.sleep(2)
gun.fire()
time.sleep(2)
gun.stop_fire()