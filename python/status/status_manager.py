#-*-coding:utf-8-*-
from datetime import datetime
import time

import threading
from websocket_server import WebsocketServer
# from sensor import SerialSensorManager


class Accelerometer(object):

    def __init__(self):
        self.acc_x = 0.
        self.acc_y = 0.
        self.acc_z = 0.
        self.gyro_x = 0.
        self.gyro_y = 0.
        self.gyro_z = 0.


class StatusManager(object):

    def __init__(self):
        self._now = time.time()
        self._datetime_now = datetime.now()
        self._acc = Accelerometer()
        self._motion = [0, 0]

        self._server = WebsocketServer(host='127.0.0.1', port=6700)
        self._server.set_fn_new_client(self.new_client)
        self._server.set_fn_client_left(self.client_left)
        self._server.set_fn_message_received(self.message_received)
        # self._sensors = SerialSensorManager()
        # self._sensors.search(["GY-521", "Papirs-01"])
    
    def new_client(self, client, server):
        print('New client {}:{} has joined.'.format(client['address'][0], client['address'][1]))
    
    def client_left(self, client, server):
        print('Client {}:{} has left.'.format(client['address'][0], client['address'][1]))

    def message_received(self, client, server, message):
        # print(message)
        data = message.split(",")
        if data[0] == 'motion':
            motion_sensor_id = int(data[2])
            status = data[3]
            self._motion[motion_sensor_id] = 0 if status == 'stop' else 1
        elif data[0] == 'acc':
            self._acc.acc_x = float(data[3])
            self._acc.acc_y = float(data[2])
            self._acc.acc_z = float(data[4])
    
    def update(self):

        ws_thread = threading.Thread(target=self._server.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        while True:
            self._now = time.time()
            self._datetime_now = datetime.now()
            # TODO 天気情報

            # TODO 強制実行アクション取得
            
            # TODO ハッシュタグ取得
            
            time.sleep(.1)

    def get_data(self):
        return {"now": self._now, "datetime": self._datetime_now, "accelerometer": self._acc, "motions": self._motion}
