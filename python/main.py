from __future__ import print_function
from operator import itemgetter
from os import environ
from time import sleep, time

from camera import Camera
from driver import Driver
from gun import Gun
import emotion


SERIAL = environ.get("DEV_SERIAL", "/dev/tty.usbserial")
BAUD = 9600

CAMERA_PORT = 0

GUN_SWEEP_DELAY = 0.1

NEUTRAL = 0
SCARED = 1
TERRIFIED = 2


def judge(face):
    """Class a face's emotion in order to decide whether they
       deserve to get shot.

       :param face: Face object containing emotion data.
    """
    if face.scores["fear"] < 0.0002 and face.scores["surprise"] < 0.4:
        return NEUTRAL
    elif face.scores["fear"] < 0.0004 and face.scores["surprise"] < 0.8:
        return SCARED
    else:
        return TERRIFIED


def step(camera, gun):
    """Body of main scan loop and entry point of the program.

       :param camera: a Camera object used to take photos and move the camera.
       :param gun: a Gun object used to fire and move the gun.
       :returns how long we took to perform one step, in seconds
                whether the gun was pointed somewhere by the step.
    """
    # Keep track of how long we take.
    start_time = time()

    # Take photo.
    camera.sweep()
    image = camera.capture()

    # Get emotional feedback.
    faces = emotion.analyze(image)

    # Decide if any faces are scared enough to be hit.
    faces = [(face, judge(face)) for face in faces]

    # If we have any terrified people, shoot them!
    pointed = False
    if len(faces) > 0:
        victim = max(faces, key=itemgetter(1))
        if victim[1] == TERRIFIED:
            gun.shoot(camera.angle(victim[0].offset))
            pointed = True
        elif victim[1] == SCARED:
            gun.face(camera.angle(victim[0].offset))
            pointed = True

    # Return how long we took, so we can sleep for an
    # appropriate amount of time.
    return time() - start_time, pointed


if __name__ == "__main__":
    # Initialise the serial driver.
    driver = Driver(SERIAL, BAUD)

    # Initialise the camera.
    camera = Camera(CAMERA_PORT, driver)

    # Initialise the gun.
    gun = Gun(driver)

    # Run the main loop.
    while True:
        elapsed, pointed = step(camera, gun)
        if not pointed:
            # Sweep the gun at a higher rate than camera scanning.
            while 3 - elapsed > 0:
                gun.sweep(8)
                sleep(GUN_SWEEP_DELAY)
                elapsed += GUN_SWEEP_DELAY
        else:
            # Simply delay after pointing at someone.
            sleep(max(0, 3 - elapsed))
