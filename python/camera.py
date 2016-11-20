from __future__ import print_function
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

from driver import CAMERA


CENTER = 45
BASE = CENTER - 45
SPREAD = 45
RAMP_FRAMES = 10


class Camera:
    def __init__(self, port, driver):
        self.vc = cv2.VideoCapture(port)
        self.pos = CENTER
        self.sweep_dir = 1
        self.driver = driver

    def __del__(self):
        del self.vc

    def sweep(self):
        """Sweep the camera back and forth, updating its last position."""
        if self.pos <= BASE or CENTER + (CENTER - BASE) <= self.pos:
            self.sweep_dir *= -1
        self.pos += SPREAD * self.sweep_dir
        self.driver.face(CAMERA, self.pos)
        print("Sweeping camera to " + str(self.pos) + "deg")

    def angle(self, offset):
        """Calculate the true angle from the centre of an object at a
           given x-offset in an image (assuming the image was taken by
           the camera at the current position).
        """
        pass

    def capture(self):
        """Capture and return a single image from the attached webcam."""
        image = None
        for i in range(RAMP_FRAMES):
            retval, image = self.vc.read()
        image_str = cv2.imencode('.jpg', image)[1].tostring()
        return image_str
