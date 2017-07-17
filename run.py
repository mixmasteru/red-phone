from src.red_alert.ringer import Ringer
from src.red_alert.speech import Speech
from threading import Event

ready = Event()
r = Ringer(ready)
r.run()
ready.wait()

print("done picked_up: "+r.picked_up)

#s = Speech()
#s.request_polly("Achtung! Der Server Frontend, in der Region EU - Frankfurt, ist nicht erreichbar")
#s.speak()