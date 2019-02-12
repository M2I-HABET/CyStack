/**
 * GPS.cpp is repsonsible for capturing telemetry data.
 */


#include <Arduino.h>
#include "GPS.h"
#include "Data.h"
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
    // Pull new data from GPS.
    retrieve_gps_data();
    // Checks for a valid satellite fix.
    if(fixation_monitor())
    {
        // If valid gps fix, take that gps data and assign it to the
        // correct onboard variables.
        store_data();
    }
    else
    {
        // If no fixation, reverts current values to
        // that of the previous cycle. This prevents the
        // craft from thinking its currently at 0 degrees Lat & Lng
        // and 0m in Altitude (which is bad).
        revert_gps_data();
    }
    Serial.println("GPS");
}


/**
 * Pulls current data from GPS module.
 */
void GPS::retrieve_gps_data()
{
    // Opens up a serial connection between the micro controller and
    // the GPS breakout board at a certain baudrate.
    Serial1.begin(9600);
    // Reads in GPS data via serial port for 1 second.
    unsigned long gps_read_in_timer = millis();
    do
    {
        // Reads in data while it is available.
        while (Serial1.available())
        {
            // Stores the brought in data to the gps object.
            gps.encode(Serial1.read());
        }
    // Count down timer for 1 second.
    } while (millis() - gps_read_in_timer < 1000);
}


/**
 * Checks for a valid gps satellite fix.
 * True = Yes. False = No.
 */
bool GPS::fixation_monitor()
{
    // Check for a GPS fix. (Does it have a signal from the satellites)
    if(gps.satellites.value() != 0 && fix_status == false)
    {
        // GPS fix has been aquired.
        fix_status = true;
    }
    // Checks the correctness of the gps data. (Worthless if less than 5)
    if(gps.satellites.value() <  5)
    {
        // If the # of satellites drops to zero. GPS fix has been lost.
        if(gps.satellites.value() == 0)
        {
            // Updates the fix status.
            fix_status = false;
        }
    }
    // True = connected, False otherwise.
    return fix_status;
}


/**
 * Takes the new gps data and assigns it to the correct variables.
 */
void GPS::store_data()
{
    // Updates all struct variables with the most current sensor data.
    recovery_latitude = gps.location.lat();
    recovery_longitude = gps.location.lng();
    // Replaces the old backup values with the new values.
    previous_latitude = recovery_latitude;
    previous_longitude = recovery_longitude;
    Serial.print("\n\nLat: "); Serial.println(recovery_latitude, 6);
    Serial.print("Lng: "); Serial.println(recovery_longitude, 6);
}


/**
 * Updates the current struct with the previous cycles values. Used incase of
 * GPS loss or sensor error so the craft doesn't instantly think its at 0m altitude.
 */
void GPS::revert_gps_data()
{
    // Reverts values to that of the previous cycle.
    recovery_latitude = previous_latitude;
    recovery_longitude = previous_longitude;
}
