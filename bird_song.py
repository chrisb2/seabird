"""Bird song electronic sculpture."""
from jq6500 import Player
from machine import UART, Pin
from hcsr04 import HCSR04
from time import sleep, ticks_ms, ticks_diff
import random

LED_DELAY_SEC = 0.25
PLAY_DIST_CM = 10
PLAY_TIME_MS = 15000  # Length of sound tracks
VOLUME = 30  # Max 30

sound = Player(UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)), volume=VOLUME)
sensor = HCSR04(trigger_pin=4, echo_pin=3, echo_timeout_us=10000)
# rgb = [Pin(25, 1), Pin(16, 1), Pin(17, 1)]
leds = [Pin(26, 1), Pin(27, 1), Pin(28, 1), Pin(29, 1),
        Pin(6, 1), Pin(7, 1), Pin(2, 1)]


def run():
    now = ticks_ms()
    playing = False
    track_no = random.randint(1, 7)
    init_leds(leds)
    sound.pause()

    while True:
        cm = sensor.distance_cm()
        print('Distance:', cm, 'cm, ', 'Playing:', playing)
        # Play track if sensor 'sees' an object and previous track has completed playing
        
        sleep(0.5)
        if cm < PLAY_DIST_CM or playing:
            blink_leds(leds);
            if ticks_diff(ticks_ms(), now) > PLAY_TIME_MS:
                playing = False
                print('Stop Playing')
                sound.pause()
            elif not playing:
                playing = True
                print('Playing track:', track_no)
                sound.play_by_index(track_no)
                now = ticks_ms()
                track_no += 1
                if track_no > 7:
                    track_no = 1
        else:
            now = ticks_ms()


def init_leds(leds):
    for led in leds:
        led.off()


def blink_leds(leds):
    for led in leds:
        led.toggle()
        sleep(LED_DELAY_SEC)
        led.toggle()
