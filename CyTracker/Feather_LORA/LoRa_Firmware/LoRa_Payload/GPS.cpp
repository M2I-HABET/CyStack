/**
 * GPS.cpp is repsonsible for capturing telemetry data.
 */

 
#include <Arduino.h>
#include "GPS.h"
#include "DATA.h"
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>
#include "Globals.h"
#include <math.h>


/**
 * Constructor used to reference all other variables & functions.
 */
GPS::GPS()
{
	
}


/**
 * Responsible for reading in a new and full NMEA sentence from the GPS module.
 */
void GPS::manager()
{
    // Directs the GPS serial port to focus on a specific pair of GPIO's onboard the micro controller.
    // RX = 10      TX = 11
    SoftwareSerial ss(11,10);
    // Opens up a serial connection between the micro controller and
    // the GPS breakout board at a certain baudrate.
    ss.begin(9600);
    // Reads in GPS data via serial port for 1 second.
    unsigned long gps_read_in_timer = millis();
    do 
    {
        // Reads in data while it is available.
        while (ss.available())
        {
            // Stores the brought in data to the gps object.
            gps.encode(ss.read());
        }
      // Count down timer for 1 second.
    } while (millis() - gps_read_in_timer < 1000);

    // Checks the correctness of the gps data. (Worthless if less than 5)
    if(gps.satellites.value() <  5)
    {
        // If the # of satellites drops to zero. GPS fix has been lost.
        if(gps.satellites.value() == 0)
        {
            // Updates onboard error detection.
            Data.current_event = 3;
        }
        // If no fixation, reverts current values to 
        // that of the previous cycle. This prevents the 
        // craft from thinking its currently at 0 degrees Lat & Lng
        // and 0m in Altitude (which is bad).
        revert_gps_data();
    }
    else
    {
        // Updates all struct variables with the most current sensor data.
        sprintf(Data.current_gps_time, "%02d:%02d:%02d ", gps.time.hour(), gps.time.minute(), gps.time.second());
        Data.current_altitude = gps.altitude.meters();
        Data.current_latitude = gps.location.lat();
        Data.current_longitude = gps.location.lng();
        Data.current_satillite_count = gps.satellites.value();
        Data.current_speed = gps.speed.mps(); 
        Data.current_distance = calculate_distance();
        // Replaces the old backup values with the new values.
        Data.previous_altitude = Data.current_altitude;
        Data.previous_latitude = Data.current_latitude;
        Data.previous_longitude = Data.current_longitude;
        Data.previous_distance = Data.current_distance;
    }
}


/**
 * Calculates the distance to the GPS Target in meters.
 */
float GPS::calculate_distance()
{

    float distance = (float)TinyGPSPlus::distanceBetween(gps.location.lat(), 
                                                         gps.location.lng(), 
                                                         /* GUI GPS Latitude */, 
                                                         /* GUI GPS Longitude */);
    return distance;
}


/**
 * Updates the current struct with the previous cycles values. Used incase of 
 * GPS loss or sensor error so the craft doesn't instantly think its at 0m altitude.
 */
void GPS::revert_gps_data()
{
    // Reverts values to that of the previous cycle.
    Data.current_altitude = Data.previous_altitude;
    Data.current_latitude = Data.previous_latitude;
    Data.current_longitude = Data.previous_longitude;
    Data.current_speed = 0.0;
    Data.current_distance = Data.previous_distance;
}
