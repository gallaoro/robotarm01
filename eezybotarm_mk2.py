import threading
import math
import time
# from adafruit_servokit import ServoKit

# !!WARNING!! Here I use the degrees from my robot arm but they depends on how you mounted
# your servo arm/attachements. Do not use this without checking them before or you will
# likely to burn your servos

class Easing:
    # Check all easing functions here: https://easings.net/
    # Here are implemented only a few of them

    @staticmethod
    def _inOutLinearFunc(x):
        return x

    @staticmethod
    def _inOutSineFunc(x):
        return -(math.cos(math.pi * x) - 1) / 2

    @staticmethod
    def _inOutCubicFunc(x):
        if (x < 0.5):
            return 4 * x * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 3) / 2

    @staticmethod
    def _inOutCircFunc(x):
        if (x < 0.5):
            return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
        else:
            return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2

    @staticmethod
    def _inOutExpoFunc(x):
        if (x == 0):
            return 0
        elif (x == 1):
            return 1
        else:
            if (x < 0.5):
                return (math.pow(2, 20 * x - 10)) / 21
            else:
                return (2 - math.pow(2, -20 * x + 10)) / 2


    @staticmethod
    def _inOutBackFunc(x):
        c1 = 1.70158
        c2 = c1 * 1.525

        if (x < 0.5):
            return (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        else:
            return (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2


    @staticmethod
    def _baseEasing(easing, callback, start, finish, time, steps):
        def calculate(step, current):
            if (step <= steps):
                value = math.trunc(easing(step/steps) * (finish-start) + start)
                callback(value)

                nextThread = threading.Timer((time/steps)/1000, calculate, [step + 1, current])
                nextThread.start()
            else:
                return

        initThread = threading.Timer(0, calculate, [1, start])
        initThread.start()
        initThread.join()
        return

    @staticmethod
    def inOutLinear(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutLinearFunc, callback, start, finish, time, steps)

    @staticmethod
    def inOutSine(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutSineFunc, callback, start, finish, time, steps)

    @staticmethod
    def inOutCubic(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutCubicFunc, callback, start, finish, time, steps)

    @staticmethod
    def inOutCirc(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutCircFunc, callback, start, finish, time, steps)

    @staticmethod
    def inOutExpo(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutExpoFunc, callback, start, finish, time, steps)

    @staticmethod
    def inOutBack(callback, start=0, finish=100, time=1000, steps=10):
        Easing._baseEasing(Easing._inOutBackFunc, callback, start, finish, time, steps)


class Robot:
    openClamp = "OPEN_CLAMP"
    closeClamp = "CLOSE_CLAMP"

    def __init__(self):
        # self.kit = kit = ServoKit(channels=16)
        self.alpha = 0 # degrees for base servo
        self.beta = 0 # degrees for main arm servo
        self.gamma = 0 # degrees for side arm servo
        self.delta = 0 # degrees for clamp servo

    @staticmethod
    def _isValidAngle(channel, angle):
        min, max = 0, 180
        if (channel == 12):
            # base
            min, max = 0, 180
        elif (channel == 13):
            # main arm, deep
            min, max = 0, 110
        elif (channel == 14):
            # side arm, height
            min, max = 0, 110
        elif (channel == 15):
            # clamp
            min, max = 0, 180

        if (angle >= min and angle <= max):
            return True
        else:
            return False

    @staticmethod
    def _transformAngle(channel, angle):
        if (channel == 15):
            # clamp
            if (isinstance(angle, str)):
                if (angle == Robot.openClamp):
                    return 180
                elif (angle == Robot.closeClamp):
                    return 0
        return angle

    def _getAngle(self, channel):
        if (channel == 12):
            return self.alpha
        elif (channel == 13):
            return self.beta
        elif (channel == 14):
            return self.gamma
        elif (channel == 15):
            return self.delta

    def __moveRaw(self, channel, angle):
        # self.kit.servo[channel].angle = angle

        if (channel == 12):
            self.alpha = angle
        elif (channel == 13):
            self.beta = angle
        elif (channel == 14):
            self.gamma = angle
        elif (channel == 15):
            self.delta = angle

        print(f'Moved {channel} to {angle}deg')

    def setup(self):
        print("Zeroing all servos")
        self.moveInstantToAngle(12, 60)
        self.moveInstantToAngle(13, 55)
        self.moveInstantToAngle(14, 55)
        self.moveInstantToAngle(15, Robot.closeClamp)
        time.sleep(1)
        print("Setup complete")

    def moveInstantToAngle(self, channel, rawAngle):
        if (channel < 0  or channel > 15): return
        if (rawAngle is not None):
            angle = Robot._transformAngle(channel, rawAngle)
            if (Robot._isValidAngle(channel, angle)):
                self.__moveRaw(channel, angle)
            else:
                print(f'Angle of {angle}deg is out of bound for channel {channel}')

    def moveEasingFromToAngle(self, channel, sAngle, eAngle, time=1000, steps=200):
        if (channel < 0  or channel > 15): return
        if (sAngle is not None and eAngle is not None ):
            startAngle = Robot._transformAngle(channel, sAngle)
            endAngle = Robot._transformAngle(channel, eAngle)
            if (Robot._isValidAngle(channel, startAngle)):
                if (Robot._isValidAngle(channel, endAngle)):

                    def printMovement(angle):
                        self.moveInstantToAngle(channel, angle)

                    Easing.inOutCubic(printMovement, startAngle, endAngle, time, steps)
                    print("END")

                else:
                    print(f'Angle of {endAngle}deg is out of bound for channel {channel}')
            else:
                print(f'Angle of {startAngle}deg is out of bound for channel {channel}')

    def moveEasingToAngle(self, channel, eAngle, easingFunc=Easing.inOutCubic, time=1000, steps=200):
        if (channel < 0  or channel > 15): return
        if (eAngle is not None ):
            startAngle = self._getAngle(channel)
            endAngle = Robot._transformAngle(channel, eAngle)
            if (Robot._isValidAngle(channel, startAngle) == True):
                if (Robot._isValidAngle(channel, endAngle)):

                    def printMovement(angle):
                        self.moveInstantToAngle(channel, angle)

                    easingFunc(printMovement, startAngle, endAngle, time, steps)

                else:
                    print(f'Angle of {endAngle}deg is out of bound for channel {channel}')
            else:
                print(f'Angle of {startAngle}deg is out of bound for channel {channel}')

    def moveLinearToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutLinear, time, steps)

    def moveCubicToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutCubic, time, steps)

    def moveSineToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutSine, time, steps)

    def moveCircToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutCirc, time, steps)

    def moveExpoToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutExpo, time, steps)

    def moveBackToAngle(self, channel, eAngle, time=1000, steps=200):
        self.moveEasingToAngle(channel, eAngle, Easing.inOutBack, time, steps)

