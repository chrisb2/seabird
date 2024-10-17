# Seabird Electronic Sculpture

A tribute to the amazing interactive sculptures of the [The Lost Gypsy](https://thelostgypsy.com/) in  [Papatowai, New Zealand](https://www.google.com/maps/place/?q=place_id:ChIJwapUtKWmLagRdHW5ZbnSops).


![Sea bird picture](./sea-bird.jpg)

## Parts

* Paua shell
* Seeed Studio [XIAO RP2040](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) or other Micropython compatible MCU
* JQ6500 MP3 Player
* HC-SR04 ultrasonic sensor
* Ultrathin speaker 8&#937;, 2W, 20mm diameter
* A [5mm diffuse RGB LED](https://www.sparkfun.com/products/12986)
* 3mm brass rod
* USB-C socket
* Approx 1 meter of thin ethernet cable
* Female header (4 pins); to plug HC-SR04 into.
* Small box

## Circuit

![Circuit Schematic](./sea-bird-schematic.png)

## Programming

Load the MP3 files to the JQ6500 as described in [https://sparks.gogo.co.nz/jq6500/index.html](https://sparks.gogo.co.nz/jq6500/index.html). Use [Thonny](https://thonny.org/) to load all the python files to the RP2040. The Micropython libraries [micropython-jq6500](https://github.com/rdagger/micropython-jq6500), [micropython-hcsr04](https://github.com/rsc1975/micropython-hcsr04) and [pi_pico_neopixel](https://github.com/blaz-r/pi_pico_neopixel) are used.

## Construction

The feet are made from brass rod soldered together and glued to the shell with epoxy glue. The female header is glued to the top of the shell with epoxy glue. Mount the circuit in a small box as shown below:

![Control Box](./control-box.jpg)