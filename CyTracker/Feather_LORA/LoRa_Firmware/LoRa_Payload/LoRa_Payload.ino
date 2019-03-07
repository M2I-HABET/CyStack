/****LIBRARIES****/
//NON HABET
#include <RH_RF95.h>
#include <TinyGPSPlus.h>

//HABET MADE
#include "Globals.h"
#include "Data.h"
#include "GPS.h"
#include "Radio.h"


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
    // and the serial port found under 'Tools' -> 'Serial Monitor'
    Serial.begin(115200);
    // Initializes the Radio.
    Radio.initialize();
    // Bootup has happened. Set flags.
    Data.node_reset = 1;
    Data.system_boot_complete = false;
}


/**
 * MAIN PROGRAM CODE.
 */
void loop()
{
    // Monitors if the LoRa just reset and changes values accordingly.
    system_boot();
    // Reads in a new NMEA sentence.
    Gps.manager();
    // Responsible for all network operations. Includes variable 
    // packaging, logic to synchronize the network, & the ability
    // to send and receive packets to and from nodes.
    Radio.manager();
}


/**
 * Flag management during and after boot process.
 */
void system_boot()
{
    // For the first # seconds of boot.
    if((millis() - Data.startup_timer >= 3000) && !Data.system_boot_complete)
    {
        // System has now been operating for # seconds.
        Data.node_reset = 0;
        // Adjust flag.
        Data.system_boot_complete = true;
    }
}
