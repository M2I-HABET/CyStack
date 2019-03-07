/****LIBRARIES****/
//NON HABET
#include <RH_RF95.h>
#include <Time.h>

//HABET MADE
#include "Globals.h"
#include "Data.h"
#include "Radio.h"


/*****CONSTRUCTORS*****/
DATA Data;
RADIO Radio;

//Directs the radio object to focus on two specific ports.
RH_RF95 rf95(8,7);


/**
 * Method initializes the main hardware components.
 */
void setup(){
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
void loop(){
    // Reads in serial port data if available.
    serial_input();
    // Monitors if the LoRa just reset and changes values accordingly.
    system_boot();
    // Ensures the gui is connected prior to starting the microcontroller's tasks.
    if(Data.gui_connection)
    {
        // Updates GUI/user with situational info.
        Data.serial_comms();
        // Responsible for grabbing all of the craft's current information,
        // turning that data into an array that can be sent out via radio.
        // Also reads in incoming messages.
        Radio.manager();
    }
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


/**
 * Reads in serial data.
 */
void serial_input()
{
    if(Serial.available())
    {
        String new_input = "";
        while(Serial.available())
        {
            char t = Serial.read();
            new_input += t;
        }
        // Creates a character array of the length of the serial input.
        char toParse[new_input.length()];
        // Converts said string to character array.
        new_input.toCharArray(toParse, new_input.length());
        // Checks for the python gui starting up and attemping to
        // establish serial connection to this microcontroller.
        if(toParse[0] == 'P' && Data.gui_connection == false)
        {
            // Responds to the gui with the microcontroller ID tag.
            Serial.write("mission_control");
            // Updates connection status.
            Data.gui_connection = true;
            // Blinks LED (on the LoRa) to show communication setup was established.
            blink_led_long();
        }
    }
}


/*
 * Blinks LED long duration.
 */
void blink_led_long()
{
    // ON
    digitalWrite(13, HIGH);
    delay(2000);
    // OFF
    digitalWrite(13, LOW);
}
