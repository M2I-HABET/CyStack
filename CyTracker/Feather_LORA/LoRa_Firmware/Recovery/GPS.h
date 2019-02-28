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

    // GPS satellite fixation status for the recovery.
  	bool fix_status = false;
	// Holds the recovery vehicle's previous latitude.
	float previous_latitude = 0.0;
	// Holds the recovery vehicle's previous longitude.
	float previous_longitude = 0.0;
	// Latitude of the recovery vehicle's gathered from GPS.
	float recovery_latitude = 0.0;
	// Longitude of the recovery vehicle's gathered from GPS.
	float recovery_longitude = 0.0;
	// Used to only read from the GPS every # seconds.
	unsigned long gps_block = 0.0;
};
#endif
