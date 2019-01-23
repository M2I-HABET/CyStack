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
	// Responsible for pulling current sensor data from peripherals.
    void update_data();
    // Retrieves the MEGA's pressure value.
    float get_i2c_mega_pressure(char buf[]);
    // Retrieves the MEGA's altitude value (calculated by pressure).
    float get_i2c_mega_altitude(char buf[]);
    // Retrieves the MEGA's temperature value (external temp).
    float get_i2c_mega_temp(char buf[]);
    // Retrieves the MEGA's roll value.
    float get_i2c_mega_roll(char buf[]);
    // Retrieves the MEGA's pitch value.
    float get_i2c_mega_pitch(char buf[]);
    // Retrieves the MEGA's yaw value.
    float get_i2c_mega_yaw(char buf[]);
    // Retrieves the MEGA's target heading angle.
    float get_i2c_target_heading(char buf[]);
    // Retrieves the MEGA's current heading angle.
    float get_i2c_current_heading(char buf[]);
    // Retrieves the MEGA's craft state.
    float get_i2c_craft_state(char buf[]);
	
	/*---------------------------------Variables---------------------------------*/
  	
	// Stores all of Eagle Eye's current flight data.
	// The difference between this struct and the one initalized in Radio.h is that this information
	// is saves gathered/used/saved locally. The Radio.h struct holds all the network information
	// being passed between crafts (nodes).
	struct Flight_Data 
	{
		/*------------------------Mega Information------------------------*/

		// Altitude of the craft.
        float mega_altitude = 0.0;
        // Roll value of the craft.
        float mega_roll = 0.0;
        // Pitch value of the craft.
        float mega_pitch = 0.0;
        // Yaw value of the craft.
        float mega_yaw = 0.0;
        // External atmosphereic pressure.
        float mega_pressure = 0.0;
        // External temperature of craft.
        float mega_external_temperature = 0.0;
        // Current angle to the target.
	    float target_heading = 0.0;
	    // Current bearing for craft.
	    float current_heading = 0.0;
	    // Movement state of the craft. This is what the craft is currently doing
	    // and not necessarily what it wants to do.
	    float craft_state = 0.0;


		/*------------------------LoRa Information------------------------*/

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
	    // Target Altitude for the craft.
	    float current_target_altitude = 10000.0;
	   	// Target Latitude for craft.
	    float current_target_latitude = 0.0;
	    // Target Longitude for craft.
	    float current_target_longitude = 0.0;
	    // Current distance to target in meters.
	    float current_target_distance = 0.0;
		// Holds the crafts previous altitude.
		float previous_altitude = 0.0;
		// Holds the crafts previous latitude.
		float previous_latitude = 0.0;
		// Holds the crafts previous longitude.
		float previous_longitude = 0.0;
	    // Holds the crafts previous target distance.
	    float previous_target_distance = 0.0;
	};
	struct Flight_Data Local;
};
#endif
