// Created by Matthew Plewa
// Creation date: 12/6/2020
// Modified: 12/7/2020
// Bassed off of http://www.airspayce.com/mikem/arduino/RadioHead/rf22_mesh_client_8pde-example.html
// and also https://learn.adafruit.com/radio-featherwing/using-the-rfm-9x-radio

// watchdog timer has issues with serial when it restarts and can cause it to hang!!
#include <Arduino.h>
#include <SPI.h>
#include <RH_RF95.h>
#include <RHMesh.h>
//#include <Adafruit_SleepyDog.h>
#include <math.h>
#include <Adafruit_GPS.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// ALL DEFINES BELLOW
#define pi 3.14159265
#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     6    // "D"

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0
//RF power
#define RFPOWER 1
// client addr
#define CLIENT_ADDRESS 1
// Other Nodes:
#define SERVER1_ADDRESS 2
#define SERVER2_ADDRESS 3
#define SERVER3_ADDRESS 4
// max message length to prevent wierd crashes
#define RH_MESH_MAX_MESSAGE_LEN 200
#define MAX_GPS_LENGTH 128

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
RHMesh manager(rf95,SERVER3_ADDRESS);
//display
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);


// what's the name of the hardware serial port?
#define GPSSerial Serial1

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
#define GPSECHO false
// this one will just be the decoder
Adafruit_GPS payload();

uint32_t timer = millis();

char gpsString[MAX_GPS_LENGTH]="";

void append(char* s, char c, uint8_t max_len) {
        int len = strlen((char*)s);
        if(len<max_len){// protects against buffer overflow
        	s[len] = c;//add char (well uint8_t)
        	s[len+1] = '\0';// need null terminator at end since overwritten in previous line
        }
}

void getBearing(float latA, float lonA,float altA, float latB,float lonB,float altB,float *Range,float *Bearing,float *Elevation,float *Altitude){
    float R = 6372.795477598*1000.0;

    float phi1 = latA*pi/180.0;
    float phi2 = latB*pi/180.0;
    float dphi = (latB-latA)*pi/180.0;
    float dlamb = (float(lonB)-float(lonA))*pi/180.0;

    float a = sin(dphi/2)*sin(dphi/2.0)+cos(phi1)*cos(phi2)*sin(dlamb/2.0)*sin(dlamb/2.0);

    float c = 2*atan(sqrt(a)/sqrt(1.0-a));
    float distance = R*c;

    float x = cos(latB*pi/180.0)*sin(pi/180.0*(lonA-lonB));
    float y = cos(latA*pi/180.0)*sin(pi/180.0*latB)-sin(pi/180.0*latA)*cos(pi/180.0*latB)*cos(pi/180.0*(lonA-lonB));


    float az =  -180/pi*atan(x/y);
    float dla = latB-latA;
    float dlo = lonB-lonA;
    az = int(abs(az)) % 90;
    float az1 = az;
    /*
    if(dla<0 && dlo>0){
        az = 180-az;
    }
    if(dla<0 && dlo<0 && az<270){
        az = 180+az;
    }
    if(dla>0 && dlo<0 && (az<180 || az>270)){
        az = 360-az;
    }
    //if(dla>0 && dlo>0 && (az<90 || az>180))
    //    az = az;
	*/

    float el = 180.0/pi*atan((altB-altA)/distance);
    float alt = altB-altA;
    if(el<0)
        el = 0;
    //return distance, az, el;
    if(dla<0 && dlo<0){
    	az=az;
    }
    if(dla<0 && dlo>0){
        	az=360-az;
        }
    if(dla>0 && dlo<0){
        	az=180-az;
        }
    if(dla>0 && dlo>0){
        	az=180+az;
        }
    *Range = distance;
	*Bearing = az;
	*Elevation = el;
	*Altitude = alt;
}


char *strtok_fr (char *s, char delim, char **save_ptr)
{
    char *tail;
    char c;

    if (s == NULL) {
        s = *save_ptr;
    }
    tail = s;
    if ((c = *tail) == '\0') {
        s = NULL;
    }
    else {
        do {
            if (c == delim) {
                *tail++ = '\0';
                break;
           }
        }while ((c = *++tail) != '\0');
    }
    *save_ptr = tail;
    return s;
}



char *strtok_f (char *s, char delim)
{
    static char *save_ptr;

    return strtok_fr (s, delim, &save_ptr);
}

bool isEmpty(char *pStart) {
  if (',' != *pStart && '*' != *pStart && pStart != NULL)
    return false;
  else
    return true;
}

bool gga2deg(char *pStart, float *angleDegrees){
	char *p = pStart;
	  if (!isEmpty(p)) {
	    char *e = strchr(p, '.');
	    if (e == NULL || e - p > 6)
	      return false;
	    float inter = atof(p);
	    int degree = inter/100; // divide by whole number gives int
	    float min = inter - float(degree*100.0);
	    *angleDegrees = float(degree)+min/60.0;
	    return true;
	  }
	  else
		  return false;
}

void setup()
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(9600);
  Serial.println("Starting up...");
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  GPS.sendCommand(PGCMD_ANTENNA);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.display();
  delay(1000);
  // Clear the buffer.
  display.clearDisplay();
  display.display();
  Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

  display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0,0);
    display.print("R:");
    display.print("m ");
    display.println("T:");
    display.println("B:");
    display.println("E");
    display.setCursor(0,0);
    display.display(); // actually display all of the above

}

uint8_t data[] = "And hello back to you from server3";
// Dont put this on the stack:
uint8_t buf[RH_MESH_MAX_MESSAGE_LEN];
char a = 'a';
int finished = 0;

float Range = 0;
float Bearing = 0;
float Elevation = 0;
float Altitude = 0;
float Latitude = 0;
float Longitude = 0;
float alt = 0;
int timer2 = 0;

void loop()
{
  uint8_t len = sizeof(buf);
  uint8_t from;
  char c = GPS.read();
  if (GPSECHO)
      if (c) Serial.print(c);
  // update own location

  if (GPS.newNMEAreceived()) {
      // a tricky thing here is if we print the NMEA sentence, or data
      // we end up not listening and catching other sentences!
      // so be very wary if using OUTPUT_ALLDATA and trying to print out data

      if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
        return; // we can fail to parse a sentence in which case we should just wait for another
  }

  if (manager.recvfromAck(buf, &len, &from))
  {
    Serial.print("got request from : 0x");
    Serial.print(from, HEX);
    Serial.print(": ");
    Serial.println((char*)buf);

    // Send a reply back to the originator client
    if (manager.sendtoWait(data, sizeof(data), from) != RH_ROUTER_ERROR_NONE)
      Serial.println("sendtoWait failed");


    char* Message_ID = strtok_f((char*)buf,',');
    char* Time = strtok_f(NULL,',');
    char* Raw_Latitude = strtok_f(NULL,',');
    char* N_S = strtok_f(NULL,',');
    char* Raw_Longitude = strtok_f(NULL,',');
    char* E_W = strtok_f(NULL,',');
    char* Speed = strtok_f(NULL,',');
    char* something = strtok_f(NULL,',');
    char* something2 = strtok_f(NULL,',');
    char* Raw_Alt = strtok_f(NULL,',');
    char* Date = strtok_f(NULL,',');
    char* Magnetic_Variation = strtok_f(NULL,',');
    char* M_E_W = strtok_f(NULL,',');
    char* Positioning_Mode = strtok_f(NULL,',');


	gga2deg(Raw_Latitude,&Latitude);

    gga2deg(Raw_Longitude,&Longitude);
    alt = atof(Raw_Alt);

    //Serial.println("heres the data");
    Serial.print("GPSData,");
    Serial.print(Latitude,8);
    Serial.print(",");
    //Serial.println(GPS.latitudeDegrees,4);
    Serial.print(Longitude,8);
    Serial.print(",");
    //Serial.println(GPS.longitudeDegrees,4);
    Serial.println(alt,8);
    //Serial.println(GPS.altitude,4);
    Serial.print("Rssi:");
    Serial.println(rf95.lastRssi());

    timer = millis();
  }
  if(millis()-timer2>2000){
	  getBearing(Latitude,-1.0*Longitude,alt, GPS.latitudeDegrees,(GPS.longitudeDegrees),GPS.altitude, &Range, &Bearing, &Elevation, &Altitude);
	  display.clearDisplay();
	  display.setTextSize(1.2);
	  display.setTextColor(SSD1306_WHITE);
	  display.setCursor(0,0);
	  display.print("R:");
	  display.print(int(Range));
	  display.print("m ");
	  display.print("T:");
	  display.print(int((millis()-timer)/1000));
	  display.println("s");
	  display.print("B:");
	  display.println(int(Bearing));
	  display.print("El:");
	  display.print(int(Elevation));
	  display.print("El:");
	  display.print(int(Altitude));
	  display.print("m ");
	  display.setCursor(0,0);
	  display.display(); // actually display all of the above
  	timer2 = millis();
  }
}
