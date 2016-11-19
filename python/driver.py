"""
Serial command reference

 - mov [servo] [position] # moves specified servo to position (in degrees)
 - fir # fires the gun

"""

from time import sleep

import serial

SERVO_WAIT_TIME = 0.2

GUN = 0
CAMERA = 1


class Driver:
    def __init__(self, serial_port, baud_rate):
        """
        Initialise the serial port and set the initial positions of the servos

        :param serial_port: address of the serial port
        :param baud_rate: baud rate at which to communicate
        """
        self.ser = serial.Serial(serial_port, baud_rate)
        self.ser.write("mov 0 0")
        self.ser.write("mov 1 45")

    def face(self, servo, position):
        """
        Set the position of a servo

        :param servo: which servo to move
        :param position: where to move the servo to (degrees)
        """
        self.ser.write("mov " + servo + " " + position)

    def shoot(self):
        """
        Fire the gun
        """
        self.ser.write("fir")

    def shoot_at(self, position):
        """
        Positions the gun servo and then fires the gun

        :param position: where to move the servo to (degrees)
        """
        self.face(GUN, position)
        sleep(SERVO_WAIT_TIME)
        self.shoot()
