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
                print("Position: {}\tCounter:{}").format(position, self.counter)
                time.sleep(0.3)
                if self.counter < len(self.speedIncrements) - 1:
                    self.counter += 1
                else:
                    self.setPosition(position)
                    self.counter = 0
                    self.speedIncrements = []
                    self.mode = 1

    def setRunning(self, isRunning):
        self.running = isRunning

    def setPosition(self, position):
        self.mode = 1
        self.position = position

    def setPositionSlow(self, position, h):
        self.mode = 2
        if (position < self.position):
            step = -1 * h
        else:
            step = h

        increment = (self.position - position) / step
        n = int(math.ceil(abs(increment)))
        for i in range(0, n):
            if i == n - 1:
                self.speedIncrements.append(position)
            else:
                self.speedIncrements.append(self.position + step * i)

    def turnToAndSleep(self, duty, sleep):
        if (self.debug):
            print "{}: Going to {}. Sleeping for {}".format(self.name, duty, sleep)
        # self.p.ChangeDutyCycle(duty)
        time.sleep(sleep)

    def stop(self):
        self.running = False
        self.position = 0
        # self.p.stop()

    def setDebug(self, debug):
        self.debug = debug

def main():
    GPIO.setmode(GPIO.BOARD)

    PIN_ARM = 38
    GPIO.setup(PIN_ARM, GPIO.OUT)
    armMotor = Motor(PIN_ARM, 'arm', Motor.CLOSE)

    PIN_CLAW = 40
    GPIO.setup(PIN_CLAW, GPIO.OUT)
    claw = Motor(PIN_CLAW, 'claw', 10.5)


    '''
    armMotor.start()
    time.sleep(2)
    armMotor.setPosition(Motor.CENTER)
    time.sleep(2)
    armMotor.setPosition(10)
    armMotor.setPositionSlow(12.5, 0.3)
    time.sleep(15)

    armMotor.stop()
    GPIO.cleanup()
    
    '''
    armMotor.start()
    claw.start()

    # test
    try:
        while True:
            input = int(raw_input('1. Drop arm\n2. Grab egg\n3. Stop'))
            if input == 1:
                armMotor.setPositionSlow(7.5, 0.2)
                time.sleep(15)
            elif input == 2:
                claw.setPosition(8.5)
                time.sleep(2)
                armMotor.setPosition(Motor.CLOSE)
                time.sleep(4)
            elif input == 3:
                claw.stop()
                armMotor.stop()
                GPIO.cleanup()
                break
    except KeyboardInterrupt:
        claw.stop()
        armMotor.stop()
        GPIO.cleanup()

    ''' 

    armMotor.start()
    claw.start()
    time.sleep(5)
    armMotor.setPositionSlow(Motor.CENTER, 0.2)
    time.sleep(20)

    claw.setPosition(8.5)
    time.sleep(1)
    armMotor.setPosition(Motor.OPEN)
    time.sleep(4)
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        armMotor.stop()
        claw.stop()
        GPIO.cleanup()
   ''' 

if __name__ == "__main__":
    main()
