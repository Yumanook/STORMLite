import LED_control4
import random

#denote the hookup of the GPIO pins, using BCM numbering
a = 26
b = 19
c = 13
d = 6
e = 5
f = 22
g = 27
h = 17

pins = [a,b,c,d,e,f,g,h]

#initialize the LED array
array = LED_control4.Charlie(pins)

#light the first column of pixels on the array for 5 seconds
def detected(specimen, perDisped):
    #where specimen is the array of coordinates on the LED array that i want to display
    #where perDisped is the number of LEDs displayed every "readoutbeam"
    displayed = [0] * perDisped
    for x in range(0, perDisped):
        displayed[x] = specimen[int(random.random()*len(specimen))]
    array.display(displayed,5)
    array.clearDisplay()
