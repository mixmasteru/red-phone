import time
import RPi.GPIO as GPIO
from threading import Thread
from time import sleep


class Ringer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.on = True
        self._ringer1 = 11
        self._ringer2 = 13
        self._button = 7

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self._ringer1, GPIO.OUT)
        GPIO.output(self._ringer1, GPIO.LOW)
        GPIO.setup(self._ringer2, GPIO.OUT)
        GPIO.output(self._ringer2, GPIO.LOW)
        GPIO.setup(self._button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self._last_state = 0
        self._last_ts = time.time()
        self._last_check = time.time()
        self._ring = 1
        self.max_ring_cnt = 2

    def ring(self, ring_cnt):
        self.max_ring_cnt = ring_cnt
        self.run()

    def run(self):
        ring_cnt = 0
        cnt = 0
        last_ts = time.time()
        try:
            print("Press CTRL+C to exit")
            while self._ring:
                if self.checkbutton():
                    self.reset_ringer()
                    return True

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

                if self.on:
                    GPIO.output(self._ringer1, GPIO.HIGH)
                    sleep(0.01)
                    GPIO.output(self._ringer1, GPIO.LOW)
                    sleep(0.01)
                    GPIO.output(self._ringer2, GPIO.HIGH)
                    sleep(0.01)
                    GPIO.output(self._ringer2, GPIO.LOW)
                    sleep(0.01)
                else:
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
            self.reset_ringer()
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
            state = GPIO.input(self._button)  # Read button state
            if not self._last_state and state:
                print("got it")
                ret = 1

            self._last_state = state
            # sleep(0.05)
            self._last_check = time.time()
        return ret

    def reset_ringer(self):
        GPIO.output(self._ringer1, GPIO.LOW)
        GPIO.output(self._ringer2, GPIO.LOW)
