from time import sleep

import serial

SERVO_WAIT_TIME = 0.5


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

        self.face(45, 0, 90)

    def face(self, camera, gun, trigger):
        """
        Set the position of a servo

        :param camera: position of camera in degrees
        :param gun: position of gun in degrees
        :param trigger: position of trigger in degrees
        """
        self.camera_pos = camera if camera is not None else self.camera_pos
        self.gun_pos = gun if gun is not None else self.gun_pos
        self.trigger_pos = trigger if trigger is not None else self.trigger_pos

        self.ser.write(str(self.camera_pos).zfill(3) + str(self.gun_pos).zfill(3) + str(self.trigger_pos).zfill(3))

    def shoot(self):
        """
        Fire the gun
        """
        self.face(None, None, 0)
        sleep(SERVO_WAIT_TIME)
        self.face(None, None, 90)

    def shoot_at(self, position):
        """
        Positions the gun servo and then fires the gun

        :param position: where to move the servo to in degrees
        """
        self.face(None, position, None)
        sleep(SERVO_WAIT_TIME)
        self.shoot()
