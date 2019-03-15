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
  // Pulses external receive led.
  void blink_receive_led();
  // Pulses external sending led.
  void blink_send_led();
  // Pulses onboard error led.
  void blink_error_led();
	
	/*---------------------------------Native Variables---------------------------------*/

	// LoRa Event. This is assigned as needed throughout the program. Signals a specific event.
  	float payload_event = 0.0;
    // Set High for # (defined below) seconds on startup to tell other nodes in the system
    // that an unexpected power cycle has occurred and they need to clear 
    // their locally held variables.
    float node_reset = 0.0;
    // Number of seconds after startup that the node_reset will be held high.
    unsigned long startup_timer = 0;
    // Turns true after # seconds of running. Used to tell if the system started 
    // up correctly.
    bool system_boot_complete = false;
    // Power status of the LED outside of the box.
    bool external_led = false;
    // Timer to switch the external_led on/off at 1/2sec.
    unsigned long ext_led_timer = 0;
    // Digital pin number of the external reset led.
    int OPERATIONAL_LED = 9;
    // Digital pin number of the external receive led.
    int RECEIVE_LED = 6;
    // Digital pin number of the external send led.
    int SEND_LED = 10;
    // Error led.
    const byte ERROR_LED = 13;
};
#endif
