/**
 * RADIO.ccp holds all functions related the radio port/module infused inside the LoRa FeatherWing 
 * development micro controller.
 */

#include <Arduino.h>
#include "Radio.h"
#include "Data.h"
#include <RH_RF95.h>
#include "Globals.h"

/**
 * Constructor used to reference all other variables & functions.
 */
RADIO::RADIO()
{
  
}


/**
 * Parses and returns the radio transmission's altitude.
 */
float RADIO::get_radio_craft_altitude(char buf[])
{
    return (Data.Parse(buf,1));
}


/**
 * Parses and returns the radio transmission's latitude.
 */
float RADIO::get_radio_craft_latitude(char buf[])
{
    return (Data.Parse(buf,2)) / 10000.0;
}


/**
 * Parses and returns the radio transmission's longitude.
 */
float RADIO::get_radio_craft_longitude(char buf[])
{
    return (Data.Parse(buf,3)) / 10000.0;
}


/**
 * Parses and returns the radio transmission's craft Event.
 */
float RADIO::get_radio_craft_event(char buf[])
{
    return (Data.Parse(buf,4));
}


/**
 * Parses and returns the radio transmission's Time Stamp (ms).
 *    LoRa  -> 0
 *    MC    -> 5
 */
float RADIO::get_radio_timestamp(char buf[], int selector)
{
    return (Data.Parse(buf, selector));
}


/**
 * Parses and returns the radio transmission's Craft ID.
 */
float RADIO::get_radio_craft_id(char buf[])
{
    return (Data.Parse(buf,10));
}


/**
 * Assigns correct pins to the radio output port. Tests connections and variables.
 */
void RADIO::initialize()
{
    // Assigns pin 13 to have an output power connection to the LoRa's onboard LED.
    pinMode(LED, OUTPUT);
    // Assigns pin 4 to have an output singal connection to the LoRa's radio port.
    pinMode(RFM95_RST, OUTPUT);
    // Sends a high signal to the radio port for intialization.
    digitalWrite(RFM95_RST, HIGH);
    // Adjust the LED to be insync with radio trasmission.
    digitalWrite(RFM95_RST, LOW);
    // 10 millisecond delay to allow for radio setup to complete before next instruction.
    delay(10);
    // Turns the radio output high to compelte setup.
    digitalWrite(RFM95_RST, HIGH);
    // Checks for the creation of the radio object and its physical connection attribute.
    if(!rf95.init())
    {
        // If invalid connection, the program will stall and pulse the onbaord led.
        while (1)
        {
            Radio.blink_led();
        }
    }
    // Checks the radio objects tuned frequency. 
    if(!rf95.setFrequency(RF95_FREQ))
    {
        // If invalid connection, the program will stall and pulse the onbaord led.
        while (1)
        {
            Radio.blink_led();
        }
    }
    // Sets the max power to be used to in the amplification of the signal being sent out.
    rf95.setTxPower(23, false);
}


/**
 * Manages all radio comms either incoming or outgoing.
 */
void RADIO::manager()
{ 
	// Reads in radio transmission if available.
	Radio.radio_receive();
	// Checks for a specific Craft ID. '999.0' signals the start of operation.
	if((998.0 < received_id && received_id < 999.9) && !Radio.checked_in)
    {   
        Serial.println("Roll Call started.");
        // Updates crafts state.
        operation_mode = Radio.ROLLCALL;
		// Responds to Mission Control with the correct ID to signal this node is here and listening.
        delay(100);
		Radio.roll_call();
	}
 
	// After Roll Call is complete, Mission Control will broadcast the start signal. Appropriate delays are
	// distributed below to initally sync the network to a 5 second split. This makes for a 10 second revolution.
	//   
	// MS - starts instantly
	// EE - delays 5 seconds
	else if(operation_mode == Radio.STANDBY)
    {
        if(554.0 < received_id && received_id < 556.0)
        {
            // Delays # seconds to offset this node from the main mission_control node.
            delay(500);
            // Updates network state.
            operation_mode = Radio.NORMAL;
        }
	}
	// Each of the crafts have # seconds to broadcast.
	else if((millis() - broadcast_timer > 1000) && (operation_mode == NORMAL))
    {
		// Resets the counter. This disables broadcasting again until 10 seconds has passed.
        broadcast_timer = millis();
		// Sends the transmission via radio.
		Radio.broadcast();
	}
}


/**
 * Responsible for reading in signals over the radio antenna.
 */
void RADIO::radio_receive()
{
    // Checks if radio message has been received.
    if (rf95.available())
    {
      	// Creates a temporary varaible to read in the incoming transmission. 
      	uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
      	// Gets the length of the above temporary varaible.
      	uint8_t len = sizeof(buf);
        // Reads in the avaiable radio transmission, then checks if it is corrupt or complete.
        if(rf95.recv(buf, &len))
        {
            // Conversion from uint8_t to string. The purpose of this is to be able to convert to an 
            // unsigned char array for parsing. 
            String str = (char*)buf;
            char to_parse[str.length()];
            str.toCharArray(to_parse,str.length());
            // Used to display the received data in the GUI.
            radio_input = buf;
            blink_led();
            Serial.print("Radio In: ");
            Serial.println(radio_input);
            
            // This whole section is comparing the currently held varaibles from the last radio update
            // to that of the newly received signal. Updates the craft's owned variables and copies
            // down the other nodes varaibles. If the timestamp indicates that this craft currently 
            // holds the most updated values for another node (ie: LoRa's time stamp is higher than the 
            // new signal's), it replaces those variables.
          
            // Reads in the time stamp for Mission Control's last broadcast.
            float temp_home_ts = Radio.get_radio_timestamp(to_parse, 5);
            // Compares the currently brought in time stamp to the one stored onboad.
            if(temp_home_ts > Radio.home_ts)
            {
                // If the incoming signal has more up-to-date versions, we overwrite our saved version with
                // the new ones.
                Radio.home_ts = temp_home_ts;
            }
            // Reads in Craft ID to see where signal came from. 
            received_id = Radio.get_radio_craft_id(to_parse);
        }
	}
}


/**
 * Alters the craft ID of the radio transmission and broadcasts back to Mission Control.
 */
void RADIO::roll_call()
{
	// Updates the Craft_ID to Eagle Eye's specific ID #.
	Radio.craft_id = 2.0;
    Serial.println("RollCall broadcast.");
	// Sends the transmission via radio.
	Radio.broadcast();
    Serial.println("Broadcasted.");
	// Updates the node's network status.
	checked_in = true;
    // Updates craft states.
    operation_mode = Radio.STANDBY;
}


/**
 * Responsible for sending out messages via the radio antenna.
 */
void RADIO::broadcast()
{
    // Updates the time object to hold the most current operation time.
    Radio.craft_ts = millis()/1000.0;
    // Updates the Network's struct to reflect the craft's most up-to-date postioning before
    // it broadcasts the signal on the Radio.
    Radio.craft_altitude = Data.current_altitude;
    Radio.craft_latitude = Data.current_latitude;
    Radio.craft_longitude = Data.current_longitude;
    Radio.craft_event = Data.current_event;
    // Casting all float values to a character array with commas saved in between values
    // allows the character array to be parsed when received by another craft.
    String temp = "";
    temp += Radio.craft_ts;
    temp += ",";
    temp += Radio.craft_altitude;
    temp += ",";
    temp += Radio.craft_latitude * 10000;
    temp += ",";
    temp += Radio.craft_longitude * 10000;
    temp += ",";
    temp += Radio.craft_event;
    temp += ",";
    temp += Radio.home_ts;
    temp += ",";
    temp += Radio.craft_id;
    // Copy contents. 
    radio_output = temp;
    // Converts from String to char array. 
    char transmission[temp.length()];
    temp.toCharArray(transmission, temp.length());
    // Sends message passed in as paramter via antenna.
    rf95.send(transmission, sizeof(transmission));
    // Pauses all operations until the micro controll has guaranteed the transmission of the
    // signal. 
    rf95.waitPacketSent();
}


/*
 * Blinks LED.
 */
void RADIO::blink_led()
{
    // ON
    digitalWrite(LED, HIGH);
    delay(50);
    // OFF
    digitalWrite(LED, LOW);
}
