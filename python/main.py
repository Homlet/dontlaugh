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

CAMERA_PORT = 1

GUN_SWEEP_DELAY = 0.1
DELAY = 1

NEUTRAL = 0
SCARED = JOLLY = 1
TERRIFIED = ECSTATIC = 2

HAPPY_MODE = True


def judge(face):
    """Class a face's emotion in order to decide whether they
       deserve to get shot.

       :param face: Face object containing emotion data.
    """
    if HAPPY_MODE:
        print(face.scores["happiness"])
        if face.scores["happiness"] < 0.1:
            return NEUTRAL
        elif face.scores["happiness"] < 0.8:
            return JOLLY
        else:
            return ECSTATIC
    else:
        if face.scores["fear"] < 0.0001 and face.scores["surprise"] < 0.1:
            return NEUTRAL
        elif face.scores["fear"] < 0.0002 and face.scores["surprise"] < 0.3:
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
    sleep(0.5)
    height, width, image = camera.capture()
    with open("test.jpg", "w") as file:
        file.write(image)

    # Get emotional feedback.
    faces = emotion.analyze(image)

    # Decide if any faces are scared enough to be hit.
    faces = [(face, judge(face)) for face in faces]

    # If we have any terrified people, shoot them!
    pointed = False
    if len(faces) > 0:
        victim = max(faces, key=itemgetter(1))
        if victim[1] == TERRIFIED:
            gun.shoot(camera.angle(width, victim[0].offset))
            pointed = True
        elif victim[1] == SCARED:
            gun.face(camera.angle(width, victim[0].offset))
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
            if elapsed > DELAY:
                elapsed = DELAY - 1
            # Sweep the gun at a higher rate than camera scanning.
            while DELAY - elapsed > 0:
                gun.sweep(2)
                sleep(GUN_SWEEP_DELAY)
                elapsed += GUN_SWEEP_DELAY
        else:
            # Simply delay after pointing at someone.
            sleep(max(0, DELAY - elapsed))
