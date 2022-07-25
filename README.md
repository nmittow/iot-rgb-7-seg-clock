# iot-rgb-7-seg-clock

RGB leds arranged to simulate the look of a 7 segment display.

![single digit rgb cycling](https://raw.githubusercontent.com/nmittow/iot-rgb-7-seg-clock/main/Media/rgb7seg.gif)
![basic animation running on clock](https://github.com/nmittow/iot-rgb-7-seg-clock/raw/main/Media/7segclock-basicanimation.gif)

Raspberry Pi &amp; ESP32 based controllers.
![Raspberry Pi controller](https://github.com/nmittow/iot-rgb-7-seg-clock/raw/main/Media/rpi-clock-controller.jpg)
![ESP32 controller](https://raw.githubusercontent.com/nmittow/iot-rgb-7-seg-clock/main/Media/esp32-controller-installed.jpg)

ESP32 version features: realtime clock, syncs to a network time server,  supports various time display animations.

All PCBs in KiCAD.

Raspberry Pi version features: all ESP32 features plus: 3.5mm audio jack and 5V relay controlled power output (for alarm audio), python library for controlling display &amp; alarm functionality (in-progress).

Motivation: I wanted an alarm that syncs with my various calendars (google, protonmail, etc) capable of 'smart' functionality like adjusting alarm time based on calendar events &amp; traffic conditions, etc., but wanted those calculations to happen locally (i.e. not google now/similar).  Love the look of 7 segment displays but wanted a bit more control of the display.

Construction: PCBs for controllers (ESP32 based &amp; Raspberry Pi cape), 7 segment digits are custom PCBs with APA102 addressable LEDs (3 per segment), daisy-chain-able.  3D Printed shrouds &amp; laser cut acrylic diffuser front, all in a stylish wooden box.  PCBs designed in KiCAD, 3D Modeling in AutoCAD & Fusion360.

![Front turned off](https://github.com/nmittow/iot-rgb-7-seg-clock/raw/main/Media/esp32-clock-frontangled.jpg)
![Assembly of clock](https://github.com/nmittow/iot-rgb-7-seg-clock/raw/main/Media/esp32-clock-assembled.jpg)
