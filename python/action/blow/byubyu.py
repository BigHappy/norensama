#-*-coding:utf-8-*-
import random
import time

from action.action_base import ActionBase

class Byubyu(ActionBase):

    SERIFS = [
        {"name": "bufobufo", "text": "ぶふぉぶふぉぶふぉお"},
        {"name": "bubababa", "text": "ぶーばばばばー"},
    ]

    def __init__(self, speaker):
        super(Byubyu, self).__init__(speaker)

    def check(self, data):
        return abs(data.get("accelerometer").acc_x) > .4

    def run(self, data):
        serif = self.SERIFS[int(random.random()*len(self.SERIFS))]
        self._sp.say(serif["name"])
        time.sleep(1.)

        return serif["text"]
        