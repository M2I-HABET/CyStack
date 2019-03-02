/**
 * Radio.h holds all declarations and varaibles related to the radio.ccp file.
 */

#ifndef Radio_h
#define Radio_h

#include <Arduino.h>

class RADIO
{
  	public:
	  // Constructor
	  RADIO();
    // Returns the transmission's time stamp.
    float get_radio_timestamp(char buf[], String selector);
    // Returns the transmission's payload's altitude.
    float get_radio_payload_altitude(char buf[]);
    // Returns the transmission's Latitude.
    float get_radio_payload_latitude(char buf[]);
    // Returns the transmission's longitude.
    float get_radio_payload_longitude(char buf[]);
    // Returns the transmission's payload event.
    float get_radio_payload_event(char buf[]);
    // Returns the transmission's payload speed.
    float get_radio_payload_speed(char buf[]);
    // Returns the transmission's recovery latitude.
    float get_radio_recovery_latitude(char buf[]);
    // Returns the transmission's recovery longitude.
    float get_radio_recovery_longitude(char buf[]);
    // Returns the transmission's craft ID.
    float get_radio_node_id(char buf[]);
    // Runs initialzation script for the Radio.
    void initialize();
    // Passively watches for incoming radio transmissions from Mission Control and other crafts.
    void manager();
    // Sends the desired signal out over the radio antenna.
    void broadcast();
    // Receives incoming transmission.
    void radio_receive();
    // Checks if packet is valid or invalid. Error detection.
    bool validate_checksum();
    // Blinks the LED on the LoRa uC (quick blink).
    void blink_led();

  	/*---------------------------------Variables---------------------------------*/

    // Chip select pin for the radio.
    const byte RFM95_CS = 8;
    // Intialization pin for radio.
    const byte RFM95_INT = 7;
    // Reset pin onboard the radio.
    const byte RFM95_RST = 4;
    // Pins used to blink an LED to signal a radio packet has been received.
    const byte LED = 13;
    // Radio frequency used throught the Eagle Eye Program. CHECK WITH HABET BEFORE EACH FLIGHT!!!!!
    #define RF95_FREQ 433.0
    // Holds current packet for parsing.
    String radio_input = "";
    // Holds the ID of the craft that just broadcasted.
    float received_id = 0.0;

    /**
     * This set of varaibles are accessed and overseen by the HABET Payload.
     */

    // Holds the current uptime (measured in seconds) for the payload.
    float payload_ts = 0.0;

    /**
     * These variables are overseen by Recovery.
     */

    // Recovery's ms Time stamp.
    float recovery_ts = 0.0;
    float recovery_latitude = 0.0;
    float recovery_longitude = 0.0;

    /**
     * These variables are overseen by Mission Control.
     */

    // Mission Control's ms Time stamp.
    float mission_control_ts = 0.0;

    // Craft ID (SPECIFIC TO THE PAYLOAD LORA ONBOARD HABET)
    float NODE_ID = 2.0;
    // Holds the delay amount between this nodes broadcast window.
    // Configured in Radio.rollcall().
    float network_node_delay = 3000.0;
      // Used in the computation of the radio system.
  	unsigned long broadcast_timer = 0;
};

#endif
