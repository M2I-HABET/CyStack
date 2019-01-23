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
	// Returns the transmission's craft's altitude.
    float get_radio_craft_altitude(char buf[]);
    // Returns the transmission's Latitude.
    float get_radio_craft_latitude(char buf[]);
    // Returns the transmission's longitude.
    float get_radio_craft_longitude(char buf[]);
    // Returns the transmission's craft event.
    float get_radio_craft_event(char buf[]);
    // Returns the transmission's craft anchor variable.
    float get_radio_craft_anchor(char buf[]);
    // Returns the transmission's craft ID.
    float get_radio_craft_id(char buf[]);
    // Returns the transmission's target throttle variable.
    float get_radio_target_throttle(char buf[]);
    // Parses and returns the radio Target Latitude.
    float get_radio_target_latitude(char buf[]);
    // Parses and returns the radio Target Longitude.
    float get_radio_target_longitude(char buf[]);
    // Returns the transmission's time stamp.
    float get_radio_timestamp(char buf[], int selector);
    // Returns the craft's anchor status.
    float get_radio_manual_direction(char buf[]);
    // Runs initialzation script for the Radio.
    void initialize();
    // Passively watches for incoming radio transmissions from Mission Control and other crafts.
    void manager();
    // Receives incoming transmission.
    void radio_receive();
    // Responds to the RollCall signal sent from Mission Control.
    void roll_call();
    // Sends the desired signal out over the radio antenna.
    void broadcast();
    // Blinks the LED on the LoRa uC (quick blink).
    void blink_led();


  	/*---------------------------------Variables---------------------------------*/ 
	
	// Chip select pin for the radio.
	const byte RFM95_CS = 8;
	// Intialization pin for radio.
	const byte RFM95_INT = 7;
	// Reset pin onboard the radio.
	const byte RFM95_RST = 4;
	// Craft ID (Used to set start times)
	const byte NODE_ID = 2;
    // Pins used to blink an LED to signal a radio packet has been received.
    const byte LED = 13;
	// Radio frequency used throught the Eagle Eye Program. CHECK WITH HABET BEFORE EACH FLIGHT!!!!!
	#define RF95_FREQ 433.0
	// Status of the craft replying to Mission Control with its node #.
	bool checked_in = false;
	// Holds the ID of the craft that just broadcasted.  
	float received_id = 0.0;
	// Holds the current received radio signal. 
    String radio_input = "";
    // Holds the current sent radio signal.
    String radio_output = "";
	// State of Radio program. 
    // ROLLCALL - Currently in RollCall process. 
    // STANDBY  - RollCall completed, waiting for user to send out start signal. 
    // NORMAL   - Radio is running in its normal operation state. 
    enum RadioStatus {NONE, ROLLCALL, STANDBY, NORMAL};
    enum RadioStatus operation_mode = NONE;
	// Stores all information related to the network of the Eagle Eye program.
	// This struct reads specific indexes and than rebroadcasts the updated transmission to
	// the other nodes in the network. 
	struct Network_Data
    {
		/**
         * These variables are modified by the network admin operating the mission_control node. 
         */
        // Automatic or Manual control of craft. 
        // 0 - Manual
        // 1 - Auto
        float authority_mode = 0.0;
    	/**
    	 * This set of varaibles are accessed and overseen by the Eagle Eye craft.
    	 */
    	// Each of these is defined in the Data.h struct. Refer to its documentation as needed.
    	float craft_ts = 0.0;
    	float craft_altitude = 0.0;
    	float craft_latitude = 0.0;
    	float craft_longitude = 0.0;
    	float craft_event = 0.0;
    	/**
    	 * These variables are overseen by Mission Control.
    	 */
        // Mission Control's ms Time stamp.
        float home_ts = 0.0;
        // This variable is the on / off switch for the craft as far as operational movement goes.
        // Having this be on the off state (0.0) does not stop data collection, only servo and 
        // motor movement. 
        float craft_anchor = 0.0;
        // User inputted target latitude for the craft. 
        float target_latitude = 0.0;
        // User inputted target longitude for the craft. 
        float target_longitude = 0.0;
        // Holds the craft's target throttle position. This is not what the craft is currently at, 
        // but what we want the craft's to have its upper limit be. For example, it will not be 
        // at a constant 40% if we set it to '40.0', but it will be able to iterate up and down from
        // that percentage of thrust. 
        float target_throttle = 0.0;
        // Movement of craft dicated by the driver while in manual mode. Independent of throttle.
        // 0 - Stopped
        // 1 - Forward
        // 2 - Left
        // 3 - Right
        // 4 - Up
        float manual_direction = 0.0;
    	/**
    	 * This varaible is updated by each craft right before the array is broadcasted.
    	 */
    	// Craft_ID is used to tell which craft is currently broadcasting the signal. This allows
    	// for Mission Control to have a sense of if information is being relayed through nodes,
    	// or if we have a direct line of communication with each node.
    	float craft_id = 0.0;
    };
    struct Network_Data Network;

  // Used in the computation of the radio system. 
  unsigned long broadcast_timer = 0;
  
};

#endif
