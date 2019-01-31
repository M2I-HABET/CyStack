/**
 * GPS.h holds objects related to the use of thermocouples.
 */

#ifndef GPS_h
#define GPS_h

#include <Arduino.h>

class GPS
{
  public:
	
	// Constructor
	GPS();
	// Responsible for reading in a new and full NMEA sentence from the GPS module.
	void manager();
	// Pulls current data from GPS module.
	void retrieve_gps_data();
	// Checks for a valid gps satellite fix.
	bool fixation_monitor();
	// Takes the new gps data and assigns it to the correct variables.
	void store_data();
	// Updates the current struct with the previous cycles values. (Prevents 0's due to gps fix loss)
	void revert_gps_data();

  	/*---------------------------------Variables---------------------------------*/
  	
    // GPS satellite fixation status for the payload.
  	bool fix_status = false;
    // Holds the crafts previous altitude.
	float previous_altitude = 0.0;
	// Holds the crafts previous latitude.
	float previous_latitude = 0.0;
	// Holds the crafts previous longitude.
	float previous_longitude = 0.0;
	// Altitude of the craft gathered from GPS.
	float payload_altitude  = 0.0;
	// Latitude of the craft gathered from GPS.
	float payload_latitude = 0.0;
	// Longitude of the craft gathered from GPS.
	float payload_longitude = 0.0;
	// Satellite Count of the craft gathered from the GPS.
	float payload_satillite_count = 0.0;
	// Speed in meters per second.
	float payload_speed = 0.0;
	// Time of flight. Used for data capture in SD card.
	char payload_gps_time[10];
};
#endif
