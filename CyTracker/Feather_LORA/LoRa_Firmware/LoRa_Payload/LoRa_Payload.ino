/****LIBRARIES****/
#include <RH_RF95.h>
#include <TinyGPSPlus.h>

#include "Globals.h"
#include "DATA.h"
#include "GPS.h"
#include "RADIO.h"


/*****CONSTRUCTORS*****/
DATA Data;
GPS Gps;
RADIO Radio;

// Directs the radio object to focus on two specific ports.
RH_RF95 rf95(8,7);
// Creates an instance of the gps class from TinyGPSPlus.
TinyGPSPlus gps;


/**
 * INITIALIZES ALL REQUIRED PERIPHIALS AND DEPENDENCIES.
 */
void setup()
{
    // Creates a serial communication line between the arduino 
    //and the serial port found under 'Tools' -> 'Serial Monitor'
    Serial.begin(115200);
    // Initializes the Radio.
    Radio.initialize();
}


/**
 * MAIN PROGRAM CODE.
 */
void loop()
{
    // Reads in a new NMEA sentence.
    Gps.manager();
    // Responsible for all network operations. Includes variable 
    // packaging, logic to synchronize the network, & the ability
    // to send and receive packets to and from nodes.
    Radio.manager();
}
