"""Bird song electronic sculpture."""
from jq6500 import Player
from machine import UART, Pin
from hcsr04 import HCSR04
from neopixel import Neopixel
import asyncio
import random

PLAY_DIST_CM = 100
PLAY_TIME_S = 15  # Length of sound tracks
VOLUME = 30  # Max 30

sound = Player(UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)), volume=VOLUME)
sensor = HCSR04(trigger_pin=4, echo_pin=3, echo_timeout_us=10000)
pixels = Neopixel(1, 0, 2, "GRB")

track_no = random.randint(1, 7)
hue_min = 0
hue_max = 65535
hue_inc = 500
hue_curr = 0


def clear_led():
    pixels.clear()
    pixels.show()
                

def play_song(track):
    print('Track: {}'.format(track_no))
    sound.play_by_index(track)
    

def stop_song():
    sound.reset()


def get_distance():
    return sensor.distance_cm()


def increment_track():
    global track_no
    
    track_no += 1
    if track_no > 7:
        track_no = 1


async def update_led():
    global hue_curr
    
    while True:
        color = pixels.colorHSV(hue_curr, 255, 255)
        pixels.fill(color)
        pixels.show()
        hue_curr += hue_inc
        if hue_curr > hue_max:
            hue_curr = hue_min
        await asyncio.sleep_ms(50)
        

async def play():
    global track_no
    
    play_song(track_no)
    led_task = asyncio.create_task(update_led())
    await asyncio.sleep(PLAY_TIME_S)
    stop_song()
    led_task.cancel()
    clear_led()


async def main():
    stop_song()
    clear_led()

    while True:
        cm = get_distance()
        print('Distance: {:.0f}cm'.format(cm))
        if cm < PLAY_DIST_CM:
            await play()
            increment_track()
        await asyncio.sleep(0.5)    


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        asyncio.new_event_loop()
