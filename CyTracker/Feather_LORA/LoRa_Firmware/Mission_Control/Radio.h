/**
 * Radio.h holds all declarations and varaibles related to the radio.ccp file.
 */

#ifndef RADIO_h
#define RADIO_h

#include <Arduino.h>

class RADIO
{
    public:
    // Constructor
    RADIO();
    // Returns the transmission's time stamp.
    float get_radio_timestamp(char buf[], String selector);
    // Returns the transmission's craft's altitude.
    float get_radio_payload_altitude(char buf[]);
    // Returns the transmission's Latitude.
    float get_radio_payload_latitude(char buf[]);
    // Returns the transmission's longitude.
    float get_radio_payload_longitude(char buf[]);
    // Returns the transmission's craft event.
    float get_radio_payload_event(char buf[]);
    // Returns the transmission's craft ID.
    float get_radio_node_id(char buf[]);
    // Runs initialzation script for the Radio.
    void initialize();
    // Passively watches for incoming radio transmissions from Mission Control and other crafts.
    void manager();
    // Responds to the RollCall signal sent from Mission Control.
    void roll_call();
    // Sends the desired signal out over the radio antenna.
    void broadcast();
    // Compares current node against others. Prevents duplicates.
    void node_check_in();
    // Receives incoming transmission.
    void radio_receive();
    // Checks if packet is valid or invalid. Error detection.
    bool validate_checksum();
    // Blinks the LED on the LoRa uC (quick blink).
    void blink_led();
    // Blinks the LED on the LoRa uC (long duration pulse).
    void blink_led_long();

    /*---------------------------------Variables---------------------------------*/

    // Chip select pin for the radio.
    const byte RFM95_CS = 8;
    // Intialization pin for radio.
    const byte RFM95_INT = 7;
    // Reset pin onboard the radio.
    const byte RFM95_RST = 4;
    // Craft ID (Used to set start times)
    const byte NODE_ID = 1;
    // Pins used to blink an LED to signal receival packet.
    const byte LED = 13;
    // Radio frequency used throught the Eagle Eye Program. CHECK WITH HABET BEFORE EACH FLIGHT!!!!!
    #define RF95_FREQ 433.0
    // Holds the ID of the craft that just broadcasted. THIS IS ANOTHER NODE, NOT MISSION CONTROL.
    float received_id = 0.0;
    // List of nodes currently logged into network.
    // mission control - 1
    // HABET - 2
    // Recovery - 3
    float node_list[3] = {1.0, 0.0, 0.0};  // In future, need to cycle through null list and fill out 0.0.
    // Holds the current received radio signal.
    String radio_input = "";
    // Holds the current sent radio signal.
    String radio_output = "";
    // Holds the most recent received singal's rssi value.
    float received_rssi = 0.0;
    // State of Radio program.
    // ROLLCALL - Currently in RollCall process.
    // STANDBY  - RollCall completed, waiting for user to send out start signal.
    // NORMAL   - Radio is running in its normal operation state.
    enum RadioStatus {NONE, ROLLCALL, STANDBY, NORMAL};
    enum RadioStatus operation_mode = NONE;

	/**
	 * This set of varaibles are accessed and overseen by the HABET Payload.
	 */

     // Each of these is defined in the Data.h file. Refer to its documentation as needed.
	float payload_ts = 0.0;
	float payload_altitude = 0.0;
	float payload_latitude = 0.0;
	float payload_longitude = 0.0;
	float payload_event = 0.0;

	/**
	 * These variables are overseen by Mission Control.
	 */

    // Mission Control's ms Time stamp.
    float mission_control_ts = 0.0;

    /**
     * This varaible is updated by each craft right before the array is broadcasted.
     */

	// Node_ID is used to tell which radio node is currently broadcasting the signal. This allows
	// for Mission Control to have a sense of if information is being relayed through nodes,
	// or if we have a direct line of communication with each node.
	float node_id = 0.0;


    // Timer is used to for the 10 second interval that the craft will broadcast when in normal.
    // operating mode. This value is in milliseconds.
    unsigned long broadcast_timer = 0;
    // Timer is used to for the 10 second interval that the craft will broadcast on for RollCall.
    // This value is in milliseconds.
    unsigned long rc_broadcast = 0;
    // Used to house node objects.
    struct Network_Node {

        // General status of node.
        // 0 - Offline
        // 1 - Online
        // 2 - Error State
        float node_status = 0.0;
        // TBD @ a later date. Heart beat of node.
        unsigned long last_contact = 0.0;
    };
    // Node declarations.
    struct Network_Node mc_node;
    struct Network_Node payload_node;
    struct Network_Node recovery_node;
    // Holds the delay amount between this nodes broadcast window.
    // Configured in Radio.rollcall().
    float network_node_delay = 0.0;
};

#endif