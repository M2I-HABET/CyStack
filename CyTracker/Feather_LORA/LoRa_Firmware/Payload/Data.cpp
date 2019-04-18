/**
 * DATA.cpp contains the struct that holds all the Crafts situational information.
 */


#include <Arduino.h>
#include "Data.h"
#include "Radio.h"
#include "GPS.h"
#include <stdlib.h>
#include "Globals.h"
#include <SD.h>
#include <SPI.h>


/**
 * Constructor used to reference all other variables & functions.
 */
DATA::DATA()
{
	
}


/**
 * Initialize the SD card and status LEDs.
 */
void DATA::initialize()
{
    // Check for valid connection to SD card.
    if(SD.begin(SD_CS))
    {
        // Invalid connection.
        while(1)
        {
            blink_error_led(); 
        }
    }
    // Configure LEDs.
    pinMode(OPERATIONAL_LED, OUTPUT);
    pinMode(ERROR_LED, OUTPUT);
    pinMode(RECEIVE_LED, OUTPUT);
    digitalWrite(ERROR_LED, LOW);
}


/**
 * Manages the bootup process and status leds.
 */
void DATA::manager()
{
    // Monitors for a powercycle.
    system_boot();
    // Turns OPERATIONAL_LED led on/off.
    system_led();
    // Stores data to sd card.
    log_data();
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
 * Flag management during and after boot process.
 */
void DATA::system_boot()
{
    // For the first # seconds of boot.
    if((millis() - startup_timer >= 3000) && !system_boot_complete)
    {
        // System has now been operating for # seconds.
        node_reset = 0;
        // Adjust flag.
        system_boot_complete = true;
    }
}


/**
 * Non-blocking alternating timer to turn the OPERATIONAL_LED on/off at intervals of 1/2 second.
 */
void DATA::system_led()
{
    if(millis() - ext_led_timer >= 300)
    {
        ext_led_timer = millis();
        // Turns external LED off.
        if(external_led)
        {
            external_led = false;
            digitalWrite(OPERATIONAL_LED, LOW);
        }
        // Turns external LED on.
        else
        {
            external_led = true;
            digitalWrite(OPERATIONAL_LED, HIGH);
        }
    }
}


/**
 * 
 */
void DATA::log_data()
{
  if(millis() - sd_timer > 1000)
  {
    sd_timer = millis();
    if (sd_card)
    {
      sd_card.print("Radio In: ");
      sd_card.println(Radio.radio_input);
      sd_card.print("Radio Out: ");
      sd_card.println(Radio.radio_output);
      sd_card.close();
    }
  }
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
