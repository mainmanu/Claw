from threading import Thread
import time
import math
import RPi.GPIO as GPIO

class Motor(Thread):
    CENTER = 7.5
    OPEN = 12.5
    CLOSE = 2.5

    def __init__(self, port, name, startPosition):
        Thread.__init__(self)
        self.port = port
        self.frequency = 50
        self.name = name
        self.p = GPIO.PWM(self.port, self.frequency)
        self.p.start(startPosition)
        self.position = startPosition
        self.running = True
        self.debug = True
        self.mode = 1
        self.speedIncrements = []
        self.counter = 0
        '''
        Mode
        1 Normal
        2 Slowly move towards point
        '''

    def run(self):
        while self.running:
            if self.mode == 1:
                self.p.ChangeDutyCycle(self.position)
                print("Position: {}").format(self.position)
                time.sleep(1)
            elif self.mode == 2:
                position = self.speedIncrements[self.counter]
                self.p.ChangeDutyCycle(position)
                print("Position: {}").format(position)
                time.sleep(0.2)
                if self.counter < len(self.speedIncrements):
                    self.counter += 1

    def setRunning(self, isRunning):
        self.running = isRunning

    def setPosition(self, position):
        self.mode = 1
        self.position = position

    def setPositionSlow(self, position):
        self.mode = 2
        increment = (self.position - position)/0.2
        n = int(math.ceil(increment))
        for i in range(0, n):
            if i == n:
                self.speedIncrements.append(position)
            else:
                self.speedIncrements.append(self.position + n*i)

    def turnToAndSleep(self, duty, sleep):
        if (self.debug):
            print "{}: Going to {}. Sleeping for {}".format(self.name, duty, sleep)
        self.p.ChangeDutyCycle(duty)
        time.sleep(sleep)

    def stop(self):
        self.running = False
        self.position = 0
        self.p.stop()

    def setDebug(self, debug):
        self.debug = debug


def main():
    PIN_ARM = 12
    PIN_CLAW = 40

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_ARM, GPIO.OUT)
    GPIO.setup(PIN_CLAW, GPIO.OUT)

    armMotor = Motor(PIN_ARM, 'arm', Motor.OPEN)
    claw = Motor(PIN_CLAW, 'arm', 9.5)
    armMotor.start()
    claw.start()
    time.sleep(5)
    armMotor.setPosition(Motor.CENTER)
    time.sleep(4)

    claw.setPosition(8.5)
    time.sleep(1)
    armMotor.setPosition(Motor.OPEN)
    time.sleep(4)

    armMotor.stop()
    claw.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    main()