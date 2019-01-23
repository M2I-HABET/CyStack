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
	// Using the current most gps data, calculates the distance to the target destination.
	// Returns a float in meters.
	float calculate_target_distance();
	// Updates the current struct with the previous cycles values. (Prevents 0's due to gps fix loss)
	void revert_gps_data();
};
#endif
