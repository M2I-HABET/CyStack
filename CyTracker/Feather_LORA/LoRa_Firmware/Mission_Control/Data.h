/**
 * Data.h is responsible for updating the programs main struct to the current most values.
 */

#ifndef DATA_h
#define DATA_h
 
#include <Arduino.h>

class DATA
{
    public:

    // Constructor
    DATA();

    // Responsible for all serial communication to python GUI.
    void serial_comms();
    // Sends appropriate infomation back to the GUI via serial. 
    void update_gui();
    // Reads in input from the GUI via serial. 
    void serial_input();
    // Parses passed in message by using commas as the identifiers.
    float Parse(char message[], int objective);
    // Parses serial input and returns the authority mode.
    float get_serial_authority_mode(char buf[]);
    // Parses serial input and returns the user's manual direction.
    float get_serial_direction(char buf[]);
    // Parses serial input and returns the target throttle.
    float get_serial_target_throttle(char buf[]);
    // Parses serial input and returns the anchor status.
    float get_serial_craft_anchor(char buf[]);
    // Parses serial input and returns the operation state of the network.
    void get_serial_op_mode(char buf[]);

    /*-----------------------------------------------------------------------------*/
    
    // Connection status to the GUI.
    bool gui_connection = false;
    // Timer used for sending serial updates to gui.
    unsigned long serial_timer = 0;
};

#endif
