#-*-coding:utf-8-*-
import random
import threading
import time

import _secret as config
# StatusManager
from status import StatusManager

from speaker import Speaker
from ifttt import Ifttt
# Action
from action import Yureyure, Hello, Joke, TimeSignal
from action.blow import Yurayura, Soyosoyo, Byubyu

class Norensama(object):

    def __init__(self):
        self._speaker = Speaker()
        self._ifttt = Ifttt({
            "api_key": config.IFTTT_APIKEY
        })

        self._status = StatusManager()
        self._actions = [
            Yureyure(self._speaker),
            Hello(self._speaker),
            Joke(self._speaker),
            TimeSignal(self._speaker),
        ]
        self._blow_actions = [
            # よわい
            Soyosoyo(self._speaker),
            # 横揺れ
            Yurayura(self._speaker),
            # 波
            Byubyu(self._speaker)
        ]
        self._blow_action_index = 1

    def select_blow_action(self, data = {}):
        acc = data.get("accelerometer")
        if acc is None:
            return
        
        print(acc.acc_x, acc.acc_y, acc.acc_z)
        acc_x = abs(acc.acc_x)
        if acc_x > .5:
            self._blow_action_index = 2
        elif acc_x > .2:
            self._blow_action_index = 1
        else:
            self._blow_action_index = 0

    def main(self):
        print("main")
        status_thread = threading.Thread(target=self._status.update)
        status_thread.daemon = True
        status_thread.start()

        self.select_blow_action()
        selected_time = time.time()
        while True:
            data = self._status.get_data()
            # 10分に一回、ゆれの音を決める
            if time.time() - selected_time > 60.:
                self.select_blow_action(data)
                # その音で、IFTTT

            # 揺れに合わせて、ゆらゆら言っている
            start = time.time()
            while time.time() - start < 6.:
                # 風のまね
                self._blow_actions[self._blow_action_index].run(data)
                # 強制起動もここでやる
                
                # RT、フォロー、された場合は、ここでいう
                if random.random() > .9:
                    # TODO ちょっとこのファイルが再生時間長いので、カットする
                    self._speaker.say("iphone")
                    
                time.sleep(3.)
            print("search action")
            # このタイミングで、反応があると、ちがうこともいう
            runable_action = [x for x in self._actions if x.check(data)]
            if runable_action:
                start = time.time()
                idx = int(random.random()*len(runable_action))
                message = runable_action[idx].run({})
                # １時間発言していないキーワードだったら、IFTTT

                print(time.time() - start)
            time.sleep(1.)

if __name__ == "__main__":
    noren = Norensama()
    noren.main()
