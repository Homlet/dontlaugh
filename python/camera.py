from driver import CAMERA


CENTER = 45
BASE = CENTER - 45
SPREAD = 45


class Camera:
    def __init__(self, interface, driver):
        self.pos = CENTER
        self.sweep_dir = 1
        self.driver = driver

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
