import time
from threading import Event
from red_alert.speech import Speech
from red_alert.ringer import Ringer


class RedPhone:

    def __init__(self):
        self.speech = Speech()
        self.ready = Event()
        self.ringer = Ringer(self.ready)
        self.wait_second = 2
        self.ring_cnt = 2

    def alert(self, text):
        self.ringer.ring(self.ring_cnt)
        self.ready.wait()
        pickup = self.ringer.picked_up
        if pickup:
            ts = time.time()
            self.speech.request_polly(text)
            diff = time.time()-ts
            if diff < self.wait_second:
                time.sleep(self.wait_second-diff)

            self.speech.speak()

        print("by")

