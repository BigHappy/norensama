#-*-coding:utf-8-*-
import time

from action_base import ActionBase

class Hello(ActionBase):

    REST_DURATION = 30.

    def __init__(self, speaker, twitter):
        super(Hello, self).__init__(speaker,twitter)

    def check(self, data):
        mot = data.get("motions")
        return len([x for x in mot if x == 1]) > 10 

    def run(self, data):
        self._tw.tweet("おはよう")
        self._sp.say("ohayo")
        time.sleep(1.)
        self._last_running_time = time.time()
