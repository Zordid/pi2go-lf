#!/usr/bin/python
#
# Pi2Go Demo Code using the Pi2Go library
#
# Created by Gareth Davies, May 2014
# Copyright 4tronix
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
#======================================================================

import pi2go, time as time_

def millis():
    return int(round(time_.time() * 1000))

def getout():
    leftLine = pi2go.irLeftLine()
    rightLine = pi2go.irRightLine()
    while (not (leftLine and rightLine)):
        pi2go.spinLeft(20)
        leftLine = pi2go.irLeftLine()
        rightLine = pi2go.irRightLine() 

def calibrateLeft():
    print "Calibrating left..."
    pi2go.setAllLEDs(400, 0, 0)
    pi2go.spinLeft(20)

    leftLine = not pi2go.irLeftLine()
    rightLine = not pi2go.irRightLine()

    while (not leftLine and not rightLine):
        leftLine = not pi2go.irLeftLine()
        rightLine = not pi2go.irRightLine()

    if (leftLine):
        while (leftLine):
             leftLine = not pi2go.irLeftLine()
             rightLine = not pi2go.irRightLine()

        while (not rightLine):
             leftLine = not pi2go.irLeftLine()
             rightLine = not pi2go.irRightLine()

        pi2go.spinRight(20)
        while (rightLine):
             rightLine = not pi2go.irRightLine()
    else:
        pi2go.spinRight(20)
        while (not leftLine):
            leftLine = not pi2go.irLeftLine()

        pi2go.spinLeft(20)
        while (leftLine):
            leftLine = not pi2go.irLeftLine()

    pi2go.stop()

    pi2go.setAllLEDs(0, 0, 0)


def calibrateRight():
    print "Calibrating right..."
    pi2go.setAllLEDs(0, 400, 0)
    pi2go.spinRight(20)

    leftLine = not pi2go.irLeftLine()
    rightLine = not pi2go.irRightLine()
    
    while (not leftLine and not rightLine):
        leftLine = not pi2go.irLeftLine()
        rightLine = not pi2go.irRightLine()

    if (rightLine):
        while (rightLine):
             leftLine = not pi2go.irLeftLine()
             rightLine = not pi2go.irRightLine()

        while (not leftLine):
             leftLine = not pi2go.irLeftLine()
             rightLine = not pi2go.irRightLine()

        pi2go.spinLeft(20)
        while (leftLine):
             leftLine = not pi2go.irLeftLine()

    else:
        pi2go.spinLeft(20)
        while (not rightLine):
            leftLine = not pi2go.irLeftLine()
            rightLine = not pi2go.irRightLine()

        pi2go.spinRight(20)
        while (rightLine):
            leftLine = not pi2go.irLeftLine()
            rightLine = not pi2go.irRightLine()

    pi2go.stop()

    pi2go.setAllLEDs(0, 0, 0)

       
pi2go.init()

vsn = pi2go.version()
try:
    if vsn != 1:
        print "This program only runs on the full Pi2Go"
    else:

        getout()
        calibrateRight()

        pi2go.setAllLEDs(0, 0, 0)
        pi2go.stop()
        baseSpeed = 30
        reassureTime = 1500

        lastTouchLeft = millis()
        lastTouchRight = millis()

        mode = "NORMAL"

        while True:
            leftLine = not pi2go.irLeftLine()
            rightLine = not pi2go.irRightLine()
            distance = pi2go.getDistance()

            if (distance < 1):
                print "Distance too low! Turning! ", distance
                pi2go.stop()

                for i in range(3):
                    pi2go.setAllLEDs(400, 0, 0)
                    time_.sleep(0.3)
                    pi2go.setAllLEDs(0, 0, 0)
                    time_.sleep(0.3)

                pi2go.spinLeft(20)
                while (not rightLine):
                    rightLine = not pi2go.irRightLine()
                while (rightLine):
                    rightLine = not pi2go.irRightLine()
                calibrateLeft()
            
            else:
                leftSpeed = baseSpeed
                rightSpeed = baseSpeed

                if (not leftLine and rightLine):
                    lastTouchLeft = millis()
                    rightSpeed = -baseSpeed 
                elif (leftLine and not rightLine):
                    lastTouchRight = millis()
                    leftSpeed = -baseSpeed
                elif (not leftLine and not rightLine):
                    if (millis() - lastTouchLeft > reassureTime):
                        calibrateLeft()
                        lastTouchLeft = millis()
                        lastTouchRight = millis()
                    elif (millis() - lastTouchRight > reassureTime):
                        calibrateRight()
                        lastTouchRight = millis()
                        lastTouchLeft = millis()

#             print "IR sensors: ", leftLine, rightLine
            pi2go.go(leftSpeed, rightSpeed)

except KeyboardInterrupt:
    print

finally:
    pi2go.cleanup()
