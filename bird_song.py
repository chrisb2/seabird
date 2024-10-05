"""Bird song electronic sculpture."""
from jq6500 import Player
from machine import Timer, UART, Pin
import machine
from hcsr04 import HCSR04
from neopixel import Neopixel
from time import ticks_ms, ticks_diff
import random
import micropython

PLAY_DIST_CM = 100
PLAY_TIME_S = 15  # Length of sound tracks
VOLUME = 30  # Max 30

# State Constants
STOPPED = 0
STARTING = 1
PLAYING = 2
STOPPING = 3

micropython.alloc_emergency_exception_buf(100)

sound = Player(UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)), volume=VOLUME)
sensor = HCSR04(trigger_pin=4, echo_pin=3, echo_timeout_us=10000)
pixels = Neopixel(1, 0, 2, "GRB")
led_timer = Timer()
main_timer = Timer()

track_no = random.randint(1, 7)
state = STOPPED
start_time_ms = ticks_ms()

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


def start_led():
    led_timer.init(period=50, mode=Timer.PERIODIC, callback=update_led)


def clear_led():
    led_timer.deinit()
    pixels.clear()
    pixels.show()
                

def play_song(track):
    sound.play_by_index(track)
    

def stop_song():
    sound.pause()


def get_distance():
    return sensor.distance_cm()


def increment_track():
    global track_no
    
    track_no += 1
    if track_no > 7:
        track_no = 1


def main_action(t):
    global state
    global start_time_ms
    
    play_time = ticks_diff(ticks_ms(), start_time_ms) / 1000
    cm = get_distance()
    # Play track if sensor 'sees' an object and previous track has
    # completed playing
    if state == PLAYING and play_time > PLAY_TIME_S:
        state = STOPPING
    elif state == STOPPED and cm < PLAY_DIST_CM:
        state = STARTING
    print('{:.0f}cm, {}, {:.0f}s'.format(cm, state, play_time))


def run():
    global state
    global start_time_ms
    global track_no
    
    stop_song()
    clear_led()
    main_timer.init(period=500, mode=Timer.PERIODIC, callback=main_action)

    while True:
        if state == STARTING:
            print('Playing track:', track_no)
            play_song(track_no)
            start_led()
            increment_track()
            # Critical section - make sure IRQ's see consistent state of these global variables
            irq_state = machine.disable_irq()
            start_time_ms = ticks_ms()
            state = PLAYING
            machine.enable_irq(irq_state)
        elif state == STOPPING:
            print('Stop Playing')
            clear_led()
            stop_song()
            # Critical section - make sure IRQ's see consistent state of these global variables
            irq_state = machine.disable_irq()
            state = STOPPED
            machine.enable_irq(irq_state)
