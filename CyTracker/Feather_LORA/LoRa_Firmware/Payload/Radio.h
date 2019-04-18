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
    // Returns the transmission's reset flag.
    float get_radio_node_reset(char buf[]);
    // Returns the transmission's craft ID.
    float get_radio_node_id(char buf[]);
    // Runs initialzation script for the Radio.
    void initialize();
    // Passively watches for incoming radio transmissions from Mission Control and other crafts.
    void manager();
    // Constructs a normal netowrk packet.
    String construct_network_packet();
    // Sends the desired signal out over the radio antenna.
    void broadcast(String packet);
    // Receives incoming transmission.
    void radio_receive();
    // Checks if packet is valid or invalid. Error detection.
    bool validate_checksum();
    // Blinks the LED on the LoRa uC (quick blink).
    void blink_led();

  	/*---------------------------------Variables---------------------------------*/

    // Chip select pin for the radio.
    int RFM95_CS = 10;   // "B"
    int RFM95_RST = 11;  // "A"
    int RFM95_INT = 6;   // "D"
    // Radio frequency used for HABET.
    #define RF95_FREQ 433.0
    // Holds the current sent radio signal.
    String radio_output = "";
    // Holds current packet for parsing.
    String radio_input = "";
    // Holds the ID of the craft that just broadcasted.
    float received_id = 0.0;
    // Holds the reset bit used to clear the timestamp of the associated node.
    float received_reset = 0.0;

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
    float node_id = 2.0;
    // Holds the delay amount between this nodes broadcast window.
    // Configured in Radio.rollcall().
    float network_node_delay = 1500.0;
      // Used in the computation of the radio system.
  	unsigned long broadcast_timer = 0;
};

#endif
