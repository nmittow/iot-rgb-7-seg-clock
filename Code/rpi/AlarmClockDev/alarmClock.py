# alarmClock.py
#
# Raspberry pi based alarm clock using APA102 LEDs
#
####################################################
from enum import Enum
import re
timeFormat = re.compile('^( ?[0-1]?[0-9]|2[0-3]):[0-5][0-9]$')

###############################################################################
# apa102pixel:
# -----------
# A single apa102 IC
#
###############################################################################
class apa102pixel:
    """Represents a single apa102 pixel"""

    colors={#Saturation   ######### 5 #########     ######### 4 #########     ######### 3 #########     ######### 2 #########     ######### 1 #########     ######### 0 #########
        "red"         :[{"r":255,"g":0  ,"b":0  },{"r":255,"g":100,"b":100},{"r":255,"g":150,"b":150},{"r":255,"g":200,"b":200},{"r":255,"g":230,"b":230},{"r":255,"g":255,"b":255}],
        "burntorange" :[{"r":255,"g":100,"b":0  },{"r":255,"g":110,"b": 20},{"r":255,"g":120,"b":100},{"r":255,"g":165,"b":155},{"r":255,"g":230,"b":210},{"r":255,"g":255,"b":255}],
        "orange"      :[{"r":255,"g":150,"b":0  },{"r":255,"g":140,"b": 20},{"r":255,"g":180,"b": 40},{"r":255,"g":220,"b":120},{"r":255,"g":240,"b":190},{"r":255,"g":255,"b":255}],
        "gold"        :[{"r":255,"g":200,"b":0  },{"r":255,"g":210,"b":  0},{"r":255,"g":230,"b":100},{"r":255,"g":240,"b":150},{"r":255,"g":255,"b":200},{"r":255,"g":255,"b":255}],
        "yellow"      :[{"r":255,"g":255,"b":0  },{"r":255,"g":255,"b": 20},{"r":255,"g":255,"b": 80},{"r":255,"g":255,"b":150},{"r":255,"g":255,"b":210},{"r":255,"g":255,"b":255}],
        "lemonlime"   :[{"r":200,"g":255,"b":0  },{"r":200,"g":255,"b": 20},{"r":220,"g":255,"b": 80},{"r":230,"g":255,"b":150},{"r":235,"g":255,"b":180},{"r":255,"g":255,"b":255}],
        "chartreuse"  :[{"r":150,"g":255,"b":0  },{"r":150,"g":255,"b": 20},{"r":200,"g":255,"b": 40},{"r":220,"g":255,"b":150},{"r":230,"g":255,"b":170},{"r":255,"g":255,"b":255}],
        "lime"        :[{"r":100,"g":255,"b":0  },{"r":110,"g":255,"b": 20},{"r":150,"g":255,"b": 40},{"r":200,"g":255,"b":150},{"r":230,"g":255,"b":160},{"r":255,"g":255,"b":255}],
        "green"       :[{"r":0  ,"g":255,"b":0  },{"r":100,"g":255,"b":100},{"r":150,"g":255,"b":250},{"r":200,"g":255,"b":200},{"r":225,"g":255,"b":225},{"r":255,"g":255,"b":255}],
        "caribbean"   :[{"r":0  ,"g":255,"b":100},{"r": 20,"g":255,"b":150},{"r":100,"g":255,"b":180},{"r":180,"g":255,"b":210},{"r":235,"g":255,"b":220},{"r":255,"g":255,"b":255}],
        "aquamarine"  :[{"r":0  ,"g":255,"b":150},{"r": 20,"g":255,"b":160},{"r":100,"g":255,"b":200},{"r":160,"g":255,"b":210},{"r":200,"g":255,"b":220},{"r":255,"g":255,"b":255}],
        "seafoam"     :[{"r":0  ,"g":255,"b":200},{"r": 20,"g":255,"b":200},{"r": 40,"g":255,"b":220},{"r":140,"g":255,"b":230},{"r":200,"g":255,"b":255},{"r":255,"g":255,"b":255}],
        "cyan"        :[{"r":0  ,"g":255,"b":255},{"r": 20,"g":255,"b":255},{"r": 40,"g":255,"b":255},{"r":150,"g":255,"b":255},{"r":180,"g":255,"b":255},{"r":255,"g":255,"b":255}],
        "teal"        :[{"r":0  ,"g":200,"b":255},{"r": 20,"g":210,"b":255},{"r": 40,"g":230,"b":255},{"r": 60,"g":240,"b":255},{"r":170,"g":255,"b":255},{"r":255,"g":255,"b":255}],
        "azure"       :[{"r":0  ,"g":150,"b":255},{"r": 20,"g":180,"b":255},{"r": 40,"g":200,"b":255},{"r": 60,"g":230,"b":255},{"r":150,"g":255,"b":255},{"r":255,"g":255,"b":255}],
        "bayern"      :[{"r":0  ,"g":100,"b":255},{"r": 20,"g":150,"b":255},{"r": 40,"g":180,"b":255},{"r": 60,"g":200,"b":255},{"r":140,"g":255,"b":255},{"r":255,"g":255,"b":255}],
        "blue"        :[{"r":0  ,"g":  0,"b":255},{"r": 20,"g":100,"b":255},{"r": 40,"g":150,"b":255},{"r": 80,"g":180,"b":255},{"r":160,"g":220,"b":255},{"r":255,"g":255,"b":255}],
        "purple"      :[{"r":100,"g":  0,"b":255},{"r":120,"g": 20,"b":255},{"r":140,"g":100,"b":255},{"r":150,"g":150,"b":255},{"r":200,"g":200,"b":255},{"r":255,"g":255,"b":255}],
        "violet"      :[{"r":150,"g":  0,"b":255},{"r":150,"g": 50,"b":255},{"r":180,"g":100,"b":255},{"r":220,"g":140,"b":255},{"r":230,"g":180,"b":255},{"r":255,"g":255,"b":255}],
        "lavender"    :[{"r":200,"g":  0,"b":255},{"r":200,"g": 20,"b":255},{"r":200,"g": 60,"b":255},{"r":240,"g": 90,"b":255},{"r":255,"g":160,"b":255},{"r":255,"g":255,"b":255}],
        "magenta"     :[{"r":255,"g":  0,"b":255},{"r":255,"g": 60,"b":255},{"r":255,"g":100,"b":240},{"r":255,"g":150,"b":250},{"r":255,"g":180,"b":255},{"r":255,"g":255,"b":255}],
        "plum"        :[{"r":255,"g":  0,"b":200},{"r":255,"g": 20,"b":220},{"r":255,"g": 40,"b":230},{"r":255,"g":140,"b":240},{"r":255,"g":170,"b":255},{"r":255,"g":255,"b":255}],
        "rose"        :[{"r":255,"g":  0,"b":150},{"r":255,"g": 20,"b":200},{"r":255,"g": 40,"b":200},{"r":255,"g":100,"b":200},{"r":255,"g":160,"b":240},{"r":255,"g":255,"b":255}],
        "salmon"      :[{"r":255,"g":  0,"b":100},{"r":255,"g": 20,"b":120},{"r":255,"g": 80,"b":140},{"r":255,"g":100,"b":160},{"r":255,"g":140,"b":180},{"r":255,"g":255,"b":255}]
    }

    def __init__(self, x=0,y=0,z=0,t=0,c=[0,0,0],brightness=31,saturation=5):
        self.xcoord = x       #X SPACIAL COORDINATE
        self.ycoord = y       #Y SPACIAL COORDINATE
        self.zcoord = z       #Z SPACIAL COORDINATE
        self.tcoord = t       #TIME COORDINATE
        self.setColor(c,brightness,saturation)

    def writeOut(self):
        return [self.bright,self.b,self.g,self.r]

    def setColor(self, color, brightness=31, saturation=5):
        ###  color: either:
        ###         color name as string from colors table, OR
        ###         [r,g,b] list of color values
        ###  brightness: apa102 LED brightness value, between 0 and 31
        ###  saturation: color saturation, 0 as white to 5 full color
        ###
        if   (brightness > 31): brightness = 31
        elif (brightness < 0 ): brightness = 0
        self.bright = 224 + brightness
        if (type(color) == str):
            if   (saturation < 0 ): saturation = 0
            elif (saturation > 5 ): saturation = 5
            saturation  = 5  - saturation
            self.r      = self.colors[color][saturation]["r"]
            self.g      = self.colors[color][saturation]["g"]
            self.b      = self.colors[color][saturation]["b"]
        elif (type(color) == list):
            self.r = color[0]
            self.g = color[1]
            self.b = color[2]

###############################################################################
# apa1027SegDigit:
# -----------
# A 7 segment digit made out of 21 apa102pixels.  Has information for displaying
# digits as well as giving them a coordinate system useful for creating
# animations.
#
###############################################################################
class apa1027SegDigit:
    """A 7 segment display made out of 21 apa102pixels"""

    digitLookupTable = [
        [1,1,1,1,1,1,0], # 0
        [0,1,1,0,0,0,0], # 1
        [1,1,0,1,1,0,1], # 2
        [1,1,1,1,0,0,1], # 3
        [0,1,1,0,0,1,1], # 4
        [1,0,1,1,0,1,1], # 5
        [1,0,1,1,1,1,1], # 6
        [1,1,1,0,0,0,0], # 7
        [1,1,1,1,1,1,1], # 8
        [1,1,1,1,0,1,1], # 9
        [0,0,0,0,0,0,0]  # OFF
    ]

    digitSegmentLookupTable = [
        [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0]], # 0
        [[0,0,0],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]], # 1
        [[1,1,1],[1,1,1],[0,0,0],[1,1,1],[1,1,1],[0,0,0],[1,1,1]], # 2
        [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[1,1,1]], # 3
        [[0,0,0],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[1,1,1],[1,1,1]], # 4
        [[1,1,1],[0,0,0],[1,1,1],[1,1,1],[0,0,0],[1,1,1],[1,1,1]], # 5
        [[1,1,1],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]], # 6
        [[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]], # 7
        [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]], # 8
        [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[1,1,1],[1,1,1]], # 9
        [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]  # OFF
    ]

    segmentPixelLookupTable = [
        [ 0, 1, 2], # A
        [ 3, 4, 5], # B
        [ 6, 7, 8], # C
        [ 9,10,11], # D
        [12,13,14], # E
        [15,16,17], # F
        [18,19,20]  # G
    ]

    pixelSegmentLookupTable = [0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6]

    class segment(Enum):
        A = 0
        B = 1
        C = 2
        D = 3
        E = 4
        F = 5
        G = 6

    def __init__(self,x=0,y=0,z=0,t=0,d=10,color=[0,0,0],brightness=31,saturation=5):
        self.pixels = []
        self.xcoord = x
        self.ycoord = y
        self.zcoord = z
        self.tcoord = t
        self.setDigit(d)

        ##### A ####
        self.pixels.append(apa102pixel(self.xcoord+1, self.ycoord+0, self.zcoord, self.tcoord+0,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+2, self.ycoord+0, self.zcoord, self.tcoord+1,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+3, self.ycoord+0, self.zcoord, self.tcoord+2,color,brightness,saturation))

        ##### B ####
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+1, self.zcoord, self.tcoord+3,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+2, self.zcoord, self.tcoord+4,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+3, self.zcoord, self.tcoord+5,color,brightness,saturation))

        ##### C ####
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+5, self.zcoord, self.tcoord+6,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+6, self.zcoord, self.tcoord+7,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+4, self.ycoord+7, self.zcoord, self.tcoord+8,color,brightness,saturation))

        ##### D ####
        self.pixels.append(apa102pixel(self.xcoord+3, self.ycoord+8, self.zcoord, self.tcoord+9,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+2, self.ycoord+8, self.zcoord, self.tcoord+10,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+1, self.ycoord+8, self.zcoord, self.tcoord+11,color,brightness,saturation))

        ##### E ####
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+7, self.zcoord, self.tcoord+12,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+6, self.zcoord, self.tcoord+13,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+5, self.zcoord, self.tcoord+14,color,brightness,saturation))

        ##### F ####
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+3, self.zcoord, self.tcoord+15,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+2, self.zcoord, self.tcoord+16,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+0, self.ycoord+1, self.zcoord, self.tcoord+17,color,brightness,saturation))

        ##### G ####
        self.pixels.append(apa102pixel(self.xcoord+1, self.ycoord+4, self.zcoord, self.tcoord+18,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+2, self.ycoord+4, self.zcoord, self.tcoord+19,color,brightness,saturation))
        self.pixels.append(apa102pixel(self.xcoord+3, self.ycoord+4, self.zcoord, self.tcoord+20,color,brightness,saturation))

    def writeOutRaw(self):
        output = []
        for i in range(21):
            output.extend(self.pixels[i].writeOut())
        return output

    def writeOut(self, digit=None):
        if ((digit is None) or (digit > 10) or (digit < 0)):
            digit = self.digit
        output = []
        for i in range(21):
            if (self.digitLookupTable[digit][self.pixelSegmentLookupTable[i]]):
                output.extend(self.pixels[i].writeOut())
            else:
                output.extend([224,0,0,0])
        return output

    def setColor(self, color, brightness=31, saturation=5, pixel=None):
        if pixel is None:
            for i in range(21):
                self.pixels[i].setColor(color, brightness, saturation)
        else:
            self.pixels[pixel].setColor(color, brightness, saturation)

    def setDigit(self, digit):
        if (digit<0): digit=0
        elif (digit>10): digit=10
        elif (digit==None): digit=10
        self.digit = digit

###############################################################################
# apa102ClockDisplay:
# -----------
# A clock display comprised of 4 apa1027SegDigits and 2 apa102pixels (HH:MM)
#
###############################################################################
class apa102ClockDisplay:
    """A clock display made out of 4 apa1027SegDigits and 2 apa102pixels """

    def __init__(self,color=[0,0,0],brightness=31,saturation=5):
        self.display = []                  # x, y, z, t, d,color,brightness,saturation
        self.display.append(apa1027SegDigit( 0, 0, 0, 0,10,color,brightness,saturation))
        self.display.append(apa1027SegDigit( 6, 0, 0,21,10,color,brightness,saturation))
        self.display.append(apa102pixel(    12, 2, 0,42,   color,brightness,saturation))
        self.display.append(apa102pixel(    12, 6, 0,43,   color,brightness,saturation))
        self.display.append(apa1027SegDigit(14, 0, 0,64,10,color,brightness,saturation))
        self.display.append(apa1027SegDigit(20, 0, 0,85,10,color,brightness,saturation))

    def setColor(self,color,brightness,saturation,index):
        if (type(index) == int):
            self.display[index].setColor(color,brightness,saturation)
        else:
            for i in range(6):
                self.display[i].setColor(color,brightness,saturation)

    def setDigit(self,index,digit):
        if ((index == 2) or (index == 3) or (index < 0) or (index > 5)):
            raise ValueError("Only elements 0, 1, 4, & 5 are digits")
        self.display[index].setDigit(digit)

    def setTime(self,timeStr):
        if (not timeFormat.match(timeStr)):
            if (timeStr[0] == " "):
                self.display[0].setDigit(10)
            else:
                self.display[0].setDigit(int(timeStr[0]))
            self.display[1].setDigit(int(timeStr[1]))
            self.display[4].setDigit(int(timeStr[3]))
            self.display[5].setDigit(int(timeStr[4]))

        else:
            if (timeStr[0] == " "):
                self.display[0].setDigit(10)
            else:
                self.display[0].setDigit(int(timeStr[0]))
            self.display[1].setDigit(int(timeStr[1]))
            self.display[4].setDigit(int(timeStr[3]))
            self.display[5].setDigit(int(timeStr[4]))

    def writeOut(self):
        output = []
        for i in range(6):
            output.extend(self.display[i].writeOut())
        return output

    def setOff(self):
        self.display[0].setDigit(10)
        self.display[1].setDigit(10)
        self.display[2].setColor([0,0,0])
        self.display[3].setColor([0,0,0])
        self.display[4].setDigit(10)
        self.display[5].setDigit(10)
