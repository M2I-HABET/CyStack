//
// Created by Matt Kreul on 1/19/21.
//

/**
 * This is the header file for the main definitions, global variables, and functions for the CyTracker "main" program
 * (CyTracker.ino).
 */
#ifndef FIRMWARE_CYTRACKERSERCOM_HANDLER_H
#define FIRMWARE_CYTRACKERSERCOM_HANDLER_H

#include <stdint.h>
#include <string.h>
#include <Uart.h>
#include <SERCOM.h>
#include <variant.h>

#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     6    // "D"
// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0
//RF power
#define RFPOWER 1
// client addr
#define CLIENT_ADDRESS 1
// Other Nodes:
#define SERVER1_ADDRESS 2
#define SERVER2_ADDRESS 3
#define SERVER3_ADDRESS 4

#define GPSECHO false

//override of RH_MESH_MAX_MESSAGE_LEN to 150
#define RH_MESH_MAX_MESSAGE_LEN 150

//declaring external variables for the Feather to use
extern Uart Serial2;
extern uint8_t appendChar;
extern uint8_t readString[RH_MESH_MAX_MESSAGE_LEN];

//declaring the SERCOM Handler and append functions.  Detailed descriptions are in the .cpp file
void SERCOM4_0_Handler();
void SERCOM4_1_Handler();
void SERCOM4_2_Handler();
void SERCOM4_3_Handler();
void append(uint8_t* , uint8_t , uint8_t );

#endif //FIRMWARE_CYTRACKERSERCOM_HANDLER_H