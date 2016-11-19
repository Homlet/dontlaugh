from operator import itemgetter
from os import environ
from time import sleep, time

from camera import Camera
from driver import Driver, GUN, CAMERA
from gun import Gun
import emotion


SERIAL = environ.get("DEV_STRESSED", "/dev/tty.usbserial")
BAUD = 9600

INTERFACE = None

NEUTRAL = 0
SCARED = 1
TERRIFIED = 2


def judge(face):
    """Class a face's emotion in order to decide whether they
       deserve to get shot.

       :param face: Face object containing emotion data.
    """
    if face.fear < 0.05 and face.surprise < 0.1:
        return NEUTRAL
    elif face.fear < 0.25 and face.surprise < 0.3:
        return SCARED
    else:
        return TERRIFIED


def step(camera, gun):
    """Body of main scan loop and entry point of the program.

       :param camera: a camera object used to take
       :param driver:
       :return how long we took to perform one step, in seconds.
    """
    # Keep track of how long we take.
    start_time = time()

    # Take photo.
    camera.sweep()
    photo = camera.capture()

    # Get emotional feedback.
    faces = emotion.analyse(photo)

    # Decide if any faces are scared enough to be hit.
    faces = [(face, judge(face)) for face in faces]

    # If we have any terrified people, shoot them!
    victim = max(faces, key=itemgetter(1))
    if victim[1] == TERRIFIED:
        driver.shoot_at(camera.angle(victim[0].offset))
    elif victim[1] == SCARED:
        driver.face(GUN, camera.angle(victim[0].offset))
    else:  # victim[1] == NEUTRAL
        gun.sweep()

    # Return how long we took, so
    return time() - start_time


if __name__ == "__main__":
    # Initialise the serial driver.
    driver = Driver(SERIAL, BAUD)
    driver.init()

    # Initialise the camera.
    camera = Camera(INTERFACE, driver)

    # Initialise the gun.
    gun = Gun(driver)

    # Run the main loop.
    while True:
        elapsed = step(camera, gun)
        sleep(max(0, 3 - elapsed))
