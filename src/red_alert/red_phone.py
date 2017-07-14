from .speech import Speech
from .ringer import Ringer
import time


class RedPhone:

    def __init__(self):
        self.speech = Speech()
        self.ringer = Ringer()
        self.wait_second = 2
        self.ring_cnt = 2

    def alert(self, text):
        pickup = self.ringer.ring(self.ring_cnt)
        if pickup:
            ts = time.time()
            self.speech.request_polly(text)
            diff = time.time()-ts
            if diff < self.wait_second:
                time.sleep(self.wait_second-diff)

            self.speech.speak()
