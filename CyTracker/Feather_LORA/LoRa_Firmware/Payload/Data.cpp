/**
 * DATA.cpp contains the struct that holds all the Crafts situational information.
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
	// Example GPS Transmission. (GGA).---------------------------------------------------------------
	//
	// $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
	//
	// Example Radio Transmission.--------------------------------------------------------------------
	//
	//                PAYLOAD LORA              MISSION CONTROL    CRAFT ID
	// Time(ms),Altitude,Latitude,Longitude,LE, | Time(ms), | Signal Origin
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
	for(i=0; i<150; i++)
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
	char parsed_section[temp_iter];
	// Iterates through the temporary array copying over the info to the variable which will be returned.
	for(i=0; i<temp_iter; i++)
	{
		// Copying of the information between arrays.
		parsed_section[i] = temp_array[i];
	}
	// Converts the final array to a float.
	float temp = atof(parsed_section);
	// Returns the desired parsed section in number (float) form.
  return temp; 
}


/**
 * Blinks the external led referring to the receive led.
 */
void DATA::blink_receive_led()
{
    // ON
    digitalWrite(RECEIVE_LED, HIGH);
    delay(100);
    // OFF
    digitalWrite(RECEIVE_LED, LOW);
}


/**
 * Blinks the external led referring to the sending led.
 */
void DATA::blink_send_led()
{
    // ON
    analogWrite(SEND_LED, HIGH);
    delay(100);
    // OFF
    analogWrite(SEND_LED, LOW);
}


/*
 * Blinks LED on error.
 */
void DATA::blink_error_led()
{
    // ON
    digitalWrite(ERROR_LED, HIGH);
    delay(100);
    // OFF
    digitalWrite(ERROR_LED, LOW);
}
