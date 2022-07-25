/***

Board: ESP32 Dev Module
Speed: 921600
Flash Freq: 80MHz
Core Debug: None
Port: /dev/ttyUSB0

Wiring:

 0 : X
 1 : Yellow
 2 : Orange
 3 : X
 4 : X
 5 : X

 0 : Red
 1 : X
 2 : X
 3 : Black


GREEN
YELLOW
ORANGE
RED
BROWN


**/
#include <SPI.h>
#include <Wire.h>;
#include <RTClib.h>
#include <WiFi.h>
#include "time.h"
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

#define FASTLED_ALL_PINS_HARDWARE_SPI
#include <FastLED.h>
#define NUMPIXELS 86
#define DATA_PIN  23
#define CLOCK_PIN 18

#include "APA1027SEG_digitMasks.h"

#define STATUS_LED 2
#define OTA_PORT 3232
#define HOSTNAME "esp32-clock"
#define OTA_HOSTNAME "esp32-clock-upload"

#define TEST_ONCOLOR  CRGB::White
#define TEST_OFFCOLOR CRGB::Red

#define AMPM false

const char* ssid       = "SSID";
const char* password   = "PASSWORD";

const char* ntpServer          = "time.cloudflare.com";
const long  gmtOffset_sec      = -8 * 3600;
const int   daylightOffset_sec = -7 * 3600;
const int32_t wifiTimeout    = 10 * 60;
const int32_t NTPSyncInterval   =  5 * 60;
RTC_DS3231 rtc;

unsigned syncState = 0;
bool ledState = false;
bool colonState = false;
DateTime lastWifiConn(uint32_t(0));
DateTime lastNTPSync(uint32_t(0));

CRGB leds[NUMPIXELS];
CRGB displayMask[NUMPIXELS];

unsigned dcount = 0;
int whiteLed = 0;

bool nonce = true;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

void setup () {
  #ifndef ESP8266
    while (!Serial); // for Leonardo/Micro/Zero
  #endif
  Serial.begin(9600);
  delay(3000); // wait for console opening
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1); //??
  }
  pinMode(STATUS_LED,OUTPUT);
  Serial.printf("Connecting to %s ", ssid);
  WiFi.mode(WIFI_STA);
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.setHostname(HOSTNAME);
  WiFi.begin(ssid, password);
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  lastWifiConn = rtc.now();
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, RGB, DATA_RATE_MHZ(4)>(leds, NUMPIXELS);  // BGR ordering is typical
  
}

void loop () {
  ArduinoOTA.handle();
  syncState = sync(syncState);
  DateTime now = rtc.now();
  if (whiteLed%8 == 0 ) {
    printDateTime(&now);
    digitalWrite(STATUS_LED,ledState = !ledState);
  }
  if (whiteLed < NUMPIXELS) {
    //leds[whiteLed] = TEST_ONCOLOR;
    //void applyDigitMask(CRGB* target, uint8_t digitIndex, uint8_t digit)
    //applyDigitMask(leds, 0,0);
    //applyDigitMask(leds, 1,1);
    //applyDigitMask(leds, 2,2);
    //applyDigitMask(leds, 3,3);
    //applyColonMask(leds, true);
    applyTimeMask(leds, &now, AMPM);
    leds[whiteLed] = TEST_ONCOLOR;
    FastLED.show();
    delay(10);
    leds[whiteLed] = TEST_OFFCOLOR;
    whiteLed++;
  }
  else whiteLed = 0;
}

unsigned sync(unsigned state) {
  switch(state){
    case 0: {
      TimeSpan uconTime = rtc.now() - lastWifiConn;
      if (WiFi.status() == WL_CONNECTED) {
        Serial.print("CONNECTED: IP address: ");
        Serial.println(WiFi.localIP());
        state++;
        lastWifiConn = rtc.now();
        if (nonce) {
          nonce = false;
          launchOTADaemon();
        }
      }
      else if (uconTime.totalseconds() > wifiTimeout){
        Serial.println("WIFI TIMOUT TRIGGERED");
        WiFi.disconnect();
        WiFi.reconnect();
        lastWifiConn = rtc.now();
      }
      break;
    }
    case 1: {
      
      TimeSpan syncTime = rtc.now() - lastNTPSync;
      //Serial.print("TIME SINCE LAST SYNC: ");
      //Serial.println(syncTime.totalseconds());
      if (syncTime.totalseconds() > NTPSyncInterval) {
        if (syncNTPTime() < 0) {
          Serial.println("NTP GET FAILURE");
        }
        else {
          Serial.println("NTP GET SUCCESS");
          lastNTPSync = rtc.now();
          lastWifiConn = rtc.now();
          state--;
        }
      }
      else {
        if (WiFi.status() == WL_CONNECTED) {
          lastWifiConn = rtc.now();
        }
      }
      break;
    }
  }
  return state;
}

void printDateTime(DateTime *dt) {
  Serial.print(dt->year(), DEC);
  Serial.print('/');
  Serial.print(dt->month(), DEC);
  Serial.print('/');
  Serial.print(dt->day(), DEC);
  Serial.print(" (");
  Serial.print(daysOfTheWeek[dt->dayOfTheWeek()]);
  Serial.print(") ");
  Serial.print(dt->hour(), DEC);
  Serial.print(':');
  Serial.print(dt->minute(), DEC);
  Serial.print(':');
  Serial.print(dt->second(), DEC);
  Serial.println();
  return;
}

int syncNTPTime() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return -1;
  }
  else {
    rtc.adjust(DateTime(timeinfo.tm_year+1900, timeinfo.tm_mon+1, timeinfo.tm_mday, timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec));
    return 0;
  }
}

int launchOTADaemon(){
  ArduinoOTA.setPort(OTA_PORT);
  ArduinoOTA.setHostname(OTA_HOSTNAME);
  ArduinoOTA
    .onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });

  ArduinoOTA.begin();
}

void applyDigitMask(CRGB* target, uint8_t digitIndex, uint8_t digit) {
  uint8_t offset = 21 * digitIndex;
  if (digitIndex > 1) offset += 2;
  for (uint8_t i=0; i<21; i++) {
    target[i+offset] -= digitMasks[digit][i];
  }
  return;
}

void applyColonMask(CRGB* target, bool state) {
  target[42] -= (state?(CRGB::Black,CRGB::Black,CRGB::Black):(CRGB::White,CRGB::White,CRGB::White));
  target[43] -= (state?(CRGB::Black,CRGB::Black,CRGB::Black):(CRGB::White,CRGB::White,CRGB::White));
  return;
}

void applyTimeMask(CRGB* target, DateTime *dt, bool ampm) {
  uint8_t hr = ampm?dt->hour()%12:dt->hour(); 
  if (hr < 10) {
    applyDigitMask(target, 0,0);
    applyDigitMask(target, 1,hr);
  }
  else if (hr > 19) {
    applyDigitMask(target, 0,2);
    applyDigitMask(target, 1,hr-20);
  }
  else {
    applyDigitMask(target, 0,1);
    applyDigitMask(target, 1,hr-10);
  }
  applyDigitMask(target, 2,(uint8_t)dt->minute()/10);
  applyDigitMask(target, 3,dt->minute()%10);
  applyColonMask(target, true);
  return;
}
