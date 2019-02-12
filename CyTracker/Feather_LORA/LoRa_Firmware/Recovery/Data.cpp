/**
 * Data.cpp contains the struct that holds all the node's situational information.
 */

#include <Arduino.h>
#include "Data.h"
#include "Radio.h"
#include "GPS.h"
#include <stdlib.h>
#include "Globals.h"

/**
 * Constructor used to reference all other variables & functions.
 */
DATA::DATA()
{

}


/**
 * Returns a parsed section of the read in parameter. The parameter 'objective' represents
 * the comma's position from the beginning of the character array.
 */
float DATA::Parse(char message[], int objective)
{
	// Example GPS Transmission. (GGA)-------------------------------------------------------------------------------------
	//
	// $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
	//
	// Example Radio Transmission.-----------------------------------------------------------------------------------------
	//
	//                    LORA                                        MISSION CONTROL                       CRAFT ID
	// Time(ms),Altitude,Latitude,Longitude,LE, | Time(ms),craft_anchor,new_throttle,TargetLat,TargetLon, | Signal Origin
	//
	// The number of commas that the program needs to pass before it started parsing the data.

	// Used to iterate through the passed in character array.
	int i = 0;
	// This iterator is used to pull the wanted part of the 'message' from the entire array.
	// Used to gather information such as how long the new parsed section is.
	int temp_iter = 0;
	// Counts the commas as the character array is iterated over.
	int comma_counter = 0;
	// Temporary string used to hold the newly parsed array.
	char temp_array[20];
  	// Iterators over the entire array.
  	for(i=0; i<120; i++)
  	{
    	// Checks to see if the current iterator's position is a comma.
    	if(message[i] == ',')
    	{
    		// If so, it iterators the comma counter by 1.
      		comma_counter++;
    	}
    	// Checks to see if the desired amount of commas has been passed.
	    else if(comma_counter == objective)
	    {
		    // Checks to see if the iterator's position is a comma, used to cause a stop in parsing.
		    if(message[i] != ',')
		    {
		    	// Copies the message's character to the temporary array.
		        temp_array[temp_iter] = message[i];
		        // Iterator used to tell how long the temporary array is.
		        temp_iter++;
		    }
	    }
  	}
	// Charater array used with a fitted length of the parsed section.
	char arr[temp_iter];
	// Iterates through the temporary array copying over the info to the variable which will be returned.
	for(i=0; i<temp_iter; i++)
	{
		// Copying of the information between arrays.
	    arr[i]=temp_array[i];
	}
	// Converts the final array to a float and returns.
	return atof(arr);
}


/**
 * Responsible for all serial communication between the GUI and mission_control microcontroller.
 */
void DATA::serial_comms()
{
	// Send useful information back to the python GUI.
	Data.update_gui();
}


/**
 * Sends mission_control & craft inforamtion back to the GUI.
 */
void DATA::update_gui()
{
	// Only sends info to update gui every 1/3 second.
	if(!Serial.available() && (millis() - Data.serial_timer >= 1500))
	{
		// Resets / starts timer.
	    Data.serial_timer = millis();
	    // Starts or updates mission control microsecond timer. (Converts to seconds w/ 2 decimal places for easy of use)
	    Radio.recovery_ts = millis()/1000.0;

    	// Holds outgoing message.
		String temp_packet = "";
		temp_packet += "$";
		temp_packet += ",";
		temp_packet += "N";
		temp_packet += ",";
  		temp_packet += Radio.payload_ts;
		temp_packet += ",";
		temp_packet += Radio.payload_altitude;
		temp_packet += ",";
		temp_packet += Radio.payload_latitude * 10000;
		temp_packet += ",";
		temp_packet += Radio.payload_longitude * 10000;
		temp_packet += ",";
		temp_packet += Radio.payload_event;
		temp_packet += ",";
		temp_packet += Radio.payload_speed;
	    temp_packet += ",";
	    temp_packet += Radio.node_id;
	    temp_packet += ",";
	    temp_packet += Radio.mission_control_ts;
	    temp_packet += ",";
	    temp_packet += Radio.recovery_ts;
	    temp_packet += ",";
	    temp_packet += Gps.recovery_latitude * 10000;
	    temp_packet += ",";
	    temp_packet += Gps.recovery_longitude * 10000;
		temp_packet += "]";
		temp_packet += Radio.radio_input;
		temp_packet += "/";
		temp_packet += Radio.radio_output;
		temp_packet += "/";
		temp_packet += Radio.received_rssi;
		temp_packet += "/";
		temp_packet += "$";

		// Defines a char array with the length needed to hold the received packet.
		char serial_packet[temp_packet.length()+1];
		// Converts from String to char array.
		temp_packet.toCharArray(serial_packet, temp_packet.length()+1);
		// Sends packet via serial to python GUI.
		Serial.write(serial_packet);
	}
}
