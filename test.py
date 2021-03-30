from eezybotarm_mk2 import Robot
import time

r = Robot()
r.setup()

time.sleep(2)

# go to initial position
r.moveLinearToAngle(12, 180, 1500)
time.sleep(4)

# try linear movement
r.moveLinearToAngle(12, 0, 2000)
time.sleep(4)

# go back to initial position
r.moveLinearToAngle(12, 180, 1500)
time.sleep(4)

# try sine movement
r.moveSineToAngle(12, 0, 2000)
time.sleep(4)

# go back to initial position
r.moveLinearToAngle(12, 180, 1500)
time.sleep(4)

# try expo movement
r.moveExpoToAngle(12, 0, 2000)
time.sleep(4)

# go back to initial position
r.moveLinearToAngle(12, 180, 1500)
time.sleep(4)

# try cubic movement
r.moveCubicToAngle(12, 0, 2000)
time.sleep(4)

# go back to initial position
r.moveLinearToAngle(12, 180, 1500)
time.sleep(4)

# try circ movement
r.moveCircToAngle(12, 0, 2000)
time.sleep(4)

# go back to initial position
r.moveLinearToAngle(12, 160, 1500)
time.sleep(4)

# try back movement
r.moveBackToAngle(12, 20, 2000)
time.sleep(4)

r.setup()