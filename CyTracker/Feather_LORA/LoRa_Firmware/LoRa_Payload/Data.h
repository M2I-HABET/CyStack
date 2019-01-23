/**
 * DATA.h is responsible for updating the programs main struct to the current most values.
 */ 

#ifndef Data_h
#define Data_h

#include <Arduino.h>
  
class DATA
{
  public:
	// Constructor
	DATA();
	// Parses passed in message by using commas as the identifiers.
	float Parse(char message[], int objective);
	
	/*---------------------------------Native Variables---------------------------------*/

	// Altitude of the craft gathered from GPS.
	float current_altitude  = 0.0;
	// Latitude of the craft gathered from GPS.
	float current_latitude = 0.0;
	// Longitude of the craft gathered from GPS.
	float current_longitude = 0.0;
	// Satellite Count of the craft gathered from the GPS.
	float current_satillite_count = 0.0;
    // Speed in meters per second.
    float current_speed = 0.0;
	// LoRa Event. This is assigned as needed throughout the program. Signals a specific event.
	float current_event = 0.0;
    // Time of flight. Used for data capture in SD card.
    char current_gps_time[10];
    // Current distance in meters.
    float current_distance = 0.0;
	// Holds the crafts previous altitude.
	float previous_altitude = 0.0;
	// Holds the crafts previous latitude.
	float previous_latitude = 0.0;
	// Holds the crafts previous longitude.
	float previous_longitude = 0.0;
    // Holds the crafts previous distance in meters.
    float previous_distance = 0.0;
};
#endif
