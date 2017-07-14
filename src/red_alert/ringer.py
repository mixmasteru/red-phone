import time
from threading import Thread
from time import sleep
from gpiozero import Button, OutputDevice


class Ringer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.on = True
        self._ringer1 = OutputDevice(11)
        self._ringer2 = OutputDevice(13)
        self._button = Button(7)

        self._ring = 1
        self.max_ring_cnt = 2

    def ring(self, ring_cnt):
        self.max_ring_cnt = ring_cnt
        self.run()

    def run(self):
        ring_cnt = 0
        cnt = 0
        try:
            print("Press CTRL+C to exit")
            while self._ring:
                if ring_cnt >= self.max_ring_cnt:
                    print("max ring")
                    return False

                # pause
                if cnt >= 25:
                    ts = time.time()
                    if ts - last_ts >= 4:
                        print(ts)
                        cnt = 0
                        ring_cnt += 1
                    continue

                print('|', end='', flush=True)
                sleep(0.01)
                print('.', end='', flush=True)
                sleep(0.01)
                print('+', end='', flush=True)
                sleep(0.01)
                print('.', end='', flush=True)
                sleep(0.01)
                cnt += 1
                last_ts = time.time()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return False

    def pickup(self):
        self._ring = 0
        print("picked up")
        self.reset_ringer()
        return True

    def checkbutton(self):
        """
        debounced button
        :return:
        """
        ret = 0
        ts = time.time()

        if ts - self._last_check <= 0.05:
            ret = 0
        else:
            state = self._button.is_pressed  # Read button state
            if self._last_state and (not state):
                print("got it")
                ret = 1

            self._last_state = state
            # sleep(0.05)
            self._last_check = time.time()
        return ret

    def reset_ringer(self):
        self._ringer1.off()
        self._ringer2.off()
