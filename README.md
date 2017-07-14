# Red Phone
This is a hack to reactivate an old telephone and use it as alert system. Its possible to play audio over the headset of the phone.

## used hardware

- old rotary phone
- [Raspberry Pi Zero](https://www.raspberrypi.org/blog/raspberry-pi-zero-w-joins-family/)
- 2 Solenoids (find on Ebay)

## used software
- [DietPi](http://dietpi.com/)
- [gpiozero python lib](https://gpiozero.readthedocs.io/en/stable/index.html)
- Python


## Requirements
```bash
sudo apt-get install python-pygame
```

## Python
```bash
virtualenv -p /usr/bin/python3.4 venv
source venv/bin/activate
pip install -r requirements.txt
```

## AWS
