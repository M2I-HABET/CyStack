/**
 * Radio.ccp holds all functions related the radio port/module infused inside the LoRa FeatherWing 
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
 * Parses and returns the radio transmission's anchor variable.
 * 0.0 -> pause
 * 1.0 -> running
 */
float RADIO::get_radio_craft_anchor(char buf[])
{
    return (Data.Parse(buf,6));
}


/**
 * Parses and returns the radio transmission's target throttle variable.
 */
float RADIO::get_radio_target_throttle(char buf[])
{
    return (Data.Parse(buf,7));
}


/**
 * Parses and returns the radio Target Latitude.
 */
float RADIO::get_radio_target_latitude(char buf[])
{
    return (Data.Parse(buf,8)) / 10000.0;
}


/**
 * Parses and returns the radio Target Longitude.
 */
float RADIO::get_radio_target_longitude(char buf[])
{
    return (Data.Parse(buf,9)) / 10000.0;
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
    // Checks to see if its time to run Roll Call. Set via GUI. 
    if(operation_mode == Radio.ROLLCALL)
    {
        // Broadcasts startup packet.
        Radio.roll_call();
    }
	// After Roll Call is complete, Mission Control will broadcast the start signal.
	else if(operation_mode == Radio.STANDBY)
    {
        // Updates craft_id to the network start signal.
        Radio.Network.craft_id = 555.0;
	}
	// Each of the crafts have # seconds to broadcast. That means each craft will broadcast every # seconds.
	else if((millis() - broadcast_timer >= 1000) && (operation_mode == Radio.NORMAL))
    {
		// Resets the counter. This disables broadcasting again until 10 seconds has passed.
		broadcast_timer = millis();
		// Sends the transmission via radio.
		Radio.broadcast();
        // Switch start signal to craft ID. Normal operations have begun. 
        if(Radio.Network.craft_id == 555.0)
        {
            Radio.Network.craft_id = 1.0;
    	}
    }
}


/**
 * Alters the craft ID of the radio transmission and broadcasts back to Mission Control.
 */
void RADIO::roll_call()
{
  // Updates the Craft_ID to the network call in signal "999.0".
  Network.craft_id = 999.0;
    // Timer of 5 seconds.
    if(millis() - rc_broadcast >= 2000)
    {
        // Resets the counter. This disabled rollcall broadcasting again until 5 seconds has passed.
        rc_broadcast = millis();
        // Sends the transmission via radio.
        Radio.broadcast();
    }
}


/**
 * Creates an array to be sent out via Radio. Fills that array with correct values and returns it.
 */
void RADIO::broadcast()
{  
    // Updates the time object to hold the most current operation time.
    Network.home_ts = millis()/1000.0;
    // Casting all float values to a character array with commas saved in between values
    // so the character array can be parsed when received by another craft.
    String temp = "";
    temp += Network.craft_ts;
    temp += ",";
    temp += Network.craft_altitude;
    temp += ",";
    temp += Network.craft_latitude * 10000;
    temp += ",";
    temp += Network.craft_longitude * 10000;
    temp += ",";
    temp += Network.craft_event;
    temp += ",";
    temp += Network.home_ts;
    temp += ",";
    temp += Network.craft_anchor;
    temp += ",";
    temp += Network.target_latitude * 10000;
    temp += ",";
    temp += Network.target_longitude * 10000;
    temp += ",";
    temp += Network.target_throttle;
    temp += ",";
    temp += Network.craft_id;
    temp += ",";
    temp += Network.manual_direction;
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


/**
 * Checks for response from node after rollcall broadcast. If not found, adds to network.
 */
void RADIO::node_check_in()
{
    // Checks for response from node after rollcall broadcast.
    if(received_id != 0.0)
    {
        // Cycles through nodes that have already checked in.
        for(int i=0;i<3;i++) //Update w/ dynamic constanst.
        {
            // Checks to see if node has already checked in. Prevents duplicates.
            if(node_list[i] == received_id)
            {   // If already found, discard repeated node.
                break;
            }
            // Node id not found in current list. (New node to check in)
            else if(node_list[i] == 0.0)
            {
                // Adds the node to the network. (Known node id's list)
                node_list[i] = received_id;
                // Checks for craft's node id.
                if(1.9 < received_id && received_id < 2.1)
                {
                    // Sets Eagle Eye's network status as connected. (Used by GUI.)
                    Radio.ee_node.node_status = 1.0;
                }
                // Checks for relay's node id. (Technically anything 3.0 and above but not implemented yet)
                else if (received_id == 3.0)
                {
                    // Sets the relay's network status as connected. (Used by GUI.)
                    Radio.relay_node.node_status = 1.0;
                }
                // Breaks FOR loop.
                break;
            }
        }
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
        // Serial.println("Incoming packet...");
        // Creates a temporary varaible to read in the incoming transmission. 
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        // Gets the length of the above temporary varaible.
        uint8_t len = sizeof(buf);
        // Reads in the avaiable radio transmission.
        if(rf95.recv(buf, &len))
        {
            // Used to display the received data in the GUI.
            radio_input = buf;
            blink_led();
            // Conversion from uint8_t to string. The purpose of this is to be able to convert to an 
            // unsigned char array for parsing. 
            String str = (char*)buf;
            char to_parse[str.length()];
            str.toCharArray(to_parse,str.length());

            // This whole section is comparing the currently held varaibles from the last radio update
            // to that of the newly received signal. Updates the LoRa's owned variables and copies
            // down the other nodes' varaibles. If the time LoRa currently holds the most updated values
            // for another node (LoRa's time stamp is higher than the new signal's), it replaces those vars.
          
            // Reads in the time stamp for Mission Control's last broadcast.
            float temp_LoRa = Radio.get_radio_timestamp(to_parse, 0);
            // Compares the currently brought in time stamp to the one stored onboad.
            if(temp_LoRa > Radio.Network.craft_ts)
            {
                // If the incoming signal has more up-to-date versions, we overwrite our saved version with
                // the new ones.
                Network.craft_ts = temp_LoRa;
                Network.craft_altitude = Radio.get_radio_craft_altitude(to_parse);
                Network.craft_latitude = Radio.get_radio_craft_latitude(to_parse);
                Network.craft_longitude = Radio.get_radio_craft_longitude(to_parse);
                Network.craft_event = Radio.get_radio_craft_event(to_parse);
            }
            // Reads in Craft ID to see where signal came from. 
            received_id = Radio.get_radio_craft_id(to_parse);
            // Compares the transmission's craftID to see if its a brand new craft. If so, it logs it. 
            Radio.node_check_in();
        }
    }
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


/*
 * Blinks LED long duration.
 */
void RADIO::blink_led_long()
{
    // ON
    digitalWrite(LED, HIGH);
    delay(2000);
    // OFF
    digitalWrite(LED, LOW);
}
