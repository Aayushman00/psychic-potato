from enum import Enum


class Hand(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class Finger(str, Enum):
    THUMB = "thumb"
    INDEX = "index"
    MIDDLE = "middle"
    RING = "ring"
    PINKY = "pinky"


FINGER_ORDER = [Finger.THUMB, Finger.INDEX, Finger.MIDDLE, Finger.RING, Finger.PINKY]
