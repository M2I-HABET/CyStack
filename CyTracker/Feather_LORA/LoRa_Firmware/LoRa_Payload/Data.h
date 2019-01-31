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
	
	/*---------------------------------Native Variables---------------------------------*/

	// LoRa Event. This is assigned as needed throughout the program. Signals a specific event.
  	float payload_event = 0.0;
};
#endif
