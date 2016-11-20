from __future__ import print_function
from time import sleep

import serial

SERVO_WAIT_TIME = 0.5

CAMERA = 0
GUN = 1
TRIGGER = 2


class Driver:
    def __init__(self, serial_port, baud_rate):
        """
        Initialise the serial port and set the initial positions of the servos

        :param serial_port: address of the serial port
        :param baud_rate: baud rate at which to communicate
        """
        self.ser = serial.Serial(serial_port, baud_rate)
        self.camera_pos = 0
        self.gun_pos = 0
        self.trigger_pos = 0
        self.set_positions(45, 0, 90)

    def face(self, servo, position):
        """
        Sets the position of a servo

        :param servo: which servo (CAMERA, GUN or TRIGGER)
        :param position: position in degrees
        """
        if servo == CAMERA:
            self.set_positions(position, None, None)
        elif servo == GUN:
            self.set_positions(None, position, None)
        elif servo == TRIGGER:
            self.set_positions(None, None, position)

    def set_positions(self, camera, gun, trigger):
        """
        Set the position of all servos

        :param camera: position of camera in degrees
        :param gun: position of gun in degrees
        :param trigger: position of trigger in degrees
        """
        self.camera_pos = camera if camera is not None else self.camera_pos
        self.gun_pos = gun if gun is not None else self.gun_pos
        self.trigger_pos = trigger if trigger is not None else self.trigger_pos
        f = lambda pos: str(pos).zfill(3)
        self.ser.write(f(self.camera_pos) +
                       f(self.gun_pos) +
                       f(self.trigger_pos))

    def shoot(self):
        """
        Fire the gun
        """
        self.set_positions(None, None, 0)
        sleep(SERVO_WAIT_TIME)
        self.set_positions(None, None, 90)

    def shoot_at(self, position):
        """
        Positions the gun servo and then fires the gun

        :param position: where to move the servo to in degrees
        """
        self.set_positions(None, position, None)
        sleep(SERVO_WAIT_TIME)
        self.shoot()
