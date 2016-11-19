from driver import GUN


CENTER = 74
BASE = CENTER - 45


class Gun:
    def __init__(self, driver):
        self.pos = CENTER
        self.sweep_dir = 1
        self.driver = driver

    def sweep(self, speed):
        """Sweep the gun back and forth at a given speed."""
        if self.pos <= BASE or CENTER + (CENTER - BASE) <= self.pos:
            self.sweep_dir *= -1
        self.pos += speed * self.sweep_dir
        self.driver.face(GUN, self.pos)
        print("Sweeping gun to " + str(self.pos) + "deg")
