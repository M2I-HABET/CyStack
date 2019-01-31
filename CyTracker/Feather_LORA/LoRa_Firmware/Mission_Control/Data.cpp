/**
 * Data.cpp contains the struct that holds all the Craft's situational information.
 */

#include <Arduino.h>
#include "Data.h"
#include "Radio.h"
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
	    Radio.mission_control_ts = millis()/1000.0;
    	// Holds outgoing message.
		String temp_packet = "";
    	// Gets set true if a packet (TO BE SENT) has been created.
		bool confirmed_packet = false;
		// Roll Call config.
		if(Radio.operation_mode == Radio.ROLLCALL)
		{
			confirmed_packet = true;
			temp_packet += "$";
			temp_packet += ",";
      		temp_packet += "R";
      		temp_packet += ",";
			temp_packet += Radio.mc_node.node_status;
			temp_packet += ",";
			temp_packet += Radio.payload_node.node_status;
			temp_packet += ",";
			temp_packet += Radio.recovery_node.node_status;
			temp_packet += ",";
			temp_packet += "$";
		}
		// Normal GUI <-> mission_control Config.
		else if((Radio.operation_mode == Radio.NORMAL) 
				 || (Radio.operation_mode == Radio.STANDBY) 
				 || (Radio.operation_mode == Radio.NONE))
		{
			confirmed_packet = true;
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
		    temp_packet += Radio.node_id;
		    temp_packet += ",";
		    temp_packet += Radio.mission_control_ts;
			temp_packet += "]";
			temp_packet += Radio.radio_input;
			temp_packet += "/";
			temp_packet += Radio.radio_output;
			temp_packet += "/";
			temp_packet += Radio.received_rssi;
			temp_packet += "/";
			temp_packet += "$";
		}
		// Ensures that the packet has been assembled in the above if/else-if statement.
		if(confirmed_packet){
			// Defines a char array with the length needed to hold the received packet.
			char serial_packet[temp_packet.length()+1];
			// Converts from String to char array.
			temp_packet.toCharArray(serial_packet, temp_packet.length()+1);
			// Sends packet via serial to python GUI.
			Serial.write(serial_packet);
		}
	}
}


/**
 * Parses serial input and returns the operational mode.
 */
void DATA::get_serial_op_mode(char buf[])
{
	// Parses out operation_mode representated as integer.
    int temp_mode = (Parse(buf,1));
    // Converts integer representation to the appropriate state.
    // Checks for state of NONE. (Network operations have yet to begin)
    if(temp_mode == 0.0)
    {
    	// Assign appropriate program state.
    	Radio.operation_mode = Radio.NONE;
    }
    // Checks if the rollcall command has been given.
    else if(temp_mode == 1.0)
    {
    	// Update the mode to begin the rollcall sequence.
    	Radio.operation_mode = Radio.ROLLCALL;
    	// Setting the node status of the mission control node to
    	// 1.0 signifies that this node is working optimally in
    	// the network.
      	Radio.mc_node.node_status = 1.0;
    }
    // Checks for user command of network standby.
    else if(temp_mode == 2.0)
    {
    	// Updates network accordingly.
    	Radio.operation_mode = Radio.STANDBY;
    }
    // Checks for the user given command to start the network.
    else if(temp_mode == 3.0)
    {
    	// Updates network to Normal operations mode.
    	// This effectively starts the network cycle.
    	// (Data will begin to flow between the checked
    	// in nodes)
    	Radio.operation_mode = Radio.NORMAL;
    }
}
