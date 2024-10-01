"""Bird song electronic sculpture."""
from jq6500 import Player
from machine import Timer, UART, Pin
from hcsr04 import HCSR04
from neopixel import Neopixel
from time import sleep, ticks_ms, ticks_diff
import random

PLAY_DIST_CM = 100
PLAY_TIME_MS = 15000  # Length of sound tracks
VOLUME = 30  # Max 30

sound = Player(UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)), volume=VOLUME)
sensor = HCSR04(trigger_pin=4, echo_pin=3, echo_timeout_us=10000)
pixels = Neopixel(1, 0, 2, "GRB")
led_timer = Timer()

hue_min = 0
hue_max = 65535
hue_inc = 500
hue_curr = 0


def update_led(t):
    global hue_curr
    color = pixels.colorHSV(hue_curr, 255, 255)
    pixels.fill(color)
    pixels.show()
    hue_curr += hue_inc
    if hue_curr > hue_max:
        hue_curr = hue_min


def clear_led():
    led_timer.deinit()
    pixels.clear()
    pixels.show()
                

def play_song(track):
    sound.play_by_index(track)
    

def stop_song():
    sound.reset()


def get_distance():
    return sensor.distance_cm()


def run():
    now = ticks_ms()
    playing = False
    track_no = random.randint(1, 7)
    stop_song()
    # clear_led()

    while True:
        sleep(0.25)
        cm = get_distance()
        print('Distance: {:.0f}cm, Playing: {}, {:.1f}s'.format(cm, playing, ticks_diff(ticks_ms(), now) / 1000))
        # Play track if sensor 'sees' an object and previous track has
        # completed playing
        if cm < PLAY_DIST_CM or playing:
            if ticks_diff(ticks_ms(), now) > PLAY_TIME_MS:
                playing = False
                print('Stop Playing')
                # clear_led()
                stop_song()
                now = ticks_ms()
            elif not playing:
                playing = True
                print('Playing track:', track_no)
                play_song(track_no)
                # led_timer.init(period=50, mode=Timer.PERIODIC, callback=update_led)
                now = ticks_ms()
                track_no += 1
                if track_no > 7:
                    track_no = 1
        else:
            now = ticks_ms()
