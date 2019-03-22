import RPi.GPIO as GPIO, time, random
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Charlie:
    '''
    Class for control of the charlieplexed SparkFun 8x7 LED Array.
    '''
    def __init__(self, pins):
        '''
        pins: type 'list', list of ints for array pins a-h, in order [a,b,c,d,e,f,g,h]
        '''
        
        if len(pins) != 8:
            print("You must specify eight, and only eight, pins.")
            raise ValueError
        
        for pin in pins:
            if type(pin) != int:
                print("Pins must be of type int.")
                raise TypeError
            GPIO.setup(pin, GPIO.OUT, initial = False)
        
        a = pins[0]
        b = pins[1]
        c = pins[2]
        d = pins[3]
        e = pins[4]
        f = pins[5]
        g = pins[6]
        h = pins[7]
        self.array = [[[h,g],[g,h],[f,h],[e,h],[d,h],[c,h],[b,h],[a,h]], \
                     [[h,f],[g,f],[f,g],[e,g],[d,g],[c,g],[b,g],[a,g]], \
                     [[h,e],[g,e],[f,e],[e,f],[d,f],[c,f],[b,f],[a,f]], \
                     [[h,d],[g,d],[f,d],[e,d],[d,e],[c,e],[b,e],[a,e]], \
                     [[h,c],[g,c],[f,c],[e,c],[d,c],[c,d],[b,d],[a,d]], \
                     [[h,b],[g,b],[f,b],[e,b],[d,b],[c,b],[b,c],[a,c]], \
                     [[h,a],[g,a],[f,a],[e,a],[d,a],[c,a],[b,a],[a,b]]]
               
        self.ALL_PINS = [a,b,c,d,e,f,g,h]
                        
    def switchOrigin(self):
        '''
        Places origin [0,0] in the diagonally opposite corner of where its current position.
        '''
        switched_array = self.array
        switched_array.reverse()
        for i in switched_array:
            i.reverse()
        self.array = switched_array
        
    def clearDisplay(self):
        '''
        Clears display.
        '''
        GPIO.setup(self.ALL_PINS, GPIO.IN)
        
    def displayPoint(self, coord):
        '''
        coord: type 'list', coordinates of single pixel to be lit
        Lights a single pixel.
        '''
        self.clearDisplay()
        GPIO.setup(self.array[coord[0]][coord[1]][0], GPIO.OUT, initial = 1)
        GPIO.setup(self.array[coord[0]][coord[1]][1], GPIO.OUT, initial = 0)
        
    def test(self):
        '''
        Displays all pixels in array, one at a time, starting with [0,0] and ending with [6,7].
        '''
        x = 0
        y = 0
        while y < 8:
            self.displayPoint([x,y])
            time.sleep(0.1)
            x += 1
            if x >= 7:
                x = 0
                y += 1
        self.clearDisplay()
        
    def display(self, pixels, duration):
        
        '''
        pixels: type 'list', list of pixels to be lit each in coordinate form [x,y]
        duration: type 'int', duration to display coordinates
        Lights specified pixels in array
        '''
        
        positives = []
        for coord in pixels:
            if self.array[coord[0]][coord[1]][0] not in positives:
                positives.append([self.array[coord[0]][coord[1]][0],[]])
        for i in positives: #[[a,[]],[b,[]],[h,[]]]
            for coord in pixels:
                if self.array[coord[0]][coord[1]][0] == i[0]:
                    if self.array[coord[0]][coord[1]][1] not in i[1]:
                        i[1].append(self.array[coord[0]][coord[1]][1])
        t = 0
        pause = 0.02/len(positives)
        while t < duration:
            for i in range(0, len(positives)):
                self.clearDisplay()
                GPIO.setup(positives[i][0], GPIO.OUT, initial = True)
                GPIO.setup(positives[i][1], GPIO.OUT, initial = False)
                time.sleep(pause)
                t += pause
        self.clearDisplay()

    def screensaver(self, duration, fill = .5):
        '''
        duration: type 'int', duration to keep screensaver on
        fill: type 'float', proportion of array to fill with pixels at any given time
        Randomly displays pixels on array.
        '''
        if fill > 1 or fill < 0:
            print("fill must be of type 'float' between 0 and 1...using default value instead.")
            fill = 0.5
        t = 0
        while t < duration:
            coords = []
            while len(coords) < fill*56:
                coord = [random.randint(0,6), random.randint(0,7)]
                if coord not in coords:
                    coords.append(coord)
            
            self.display(coords, 0.15)
            t += 0.1
