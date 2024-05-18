from jq6500 import Player
from machine import UART, Pin


def run():
    uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    p = Player(uart0, volume=8)
    # p.play()
    p.play_by_index(1)
    # p.clean_up()
