/****LIBRARIES****/

//NON EAGLE EYE
#include <RH_RF95.h>
#include <Time.h>

//EAGLE EYE'S
#include "Globals.h"
#include "Data.h"
#include "Radio.h"


/*****CONSTRUCTORS*****/ //(Objects that can reference their respective functions & variables)
DATA Data;
RADIO Radio;

//Directs the radio object to focus on two specific ports.
RH_RF95 rf95(8,7);


/**
 * Method initializes the main hardware components.
 */
void setup(){
    
    // Creates a serial communication line between the arduino and the serial port 
    // found under 'Tools' -> 'Serial Monitor'
    Serial.begin(115200);
    // Initializes the Radio.
    Radio.initialize();
}


/**
 * MAIN PROGRAM CODE.
 */
void loop(){
    // Reads in serial port data if available.
    serial_input();
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
        // Checks for the python gui starting up and attemping to establish serial connection
        // to this microcontroller.
        if(toParse[0] == 'P' && Data.gui_connection == false)
        {
            // Responds to the gui with the microcontroller ID tag.
            Serial.write("MC_LORA");
            // Updates connection status.
            Data.gui_connection = true;
            // Blinks LED (on the LoRa) to show communication setup was established.
            Radio.blink_led_long();
        }
        // Checks for correct data format and prior connection status to the gui.
        else if(toParse[0] == '$' && Data.gui_connection == true)
        {
            // '0' at index 3 signifies manual control. 
            if(toParse[2]=='0')
            {
                Radio.Network.authority_mode = Data.get_serial_authority_mode(toParse);
                Radio.Network.manual_direction = Data.get_serial_direction(toParse);
                Radio.Network.craft_anchor = Data.get_serial_craft_anchor(toParse);
                Radio.Network.target_throttle = Data.get_serial_target_throttle(toParse);
                // Directly sets variables due to operation_mode being an enum state.
                Data.get_serial_op_mode(toParse);
            }
            // '1' at index 3 signifies automatic control. 
            else if(toParse[2]=='1')
            {
                // To be implemented at a later date.
            }
        }
    }
}
