//
// Created by Matt Kreul on 1/19/21.
//

#ifndef FIRMWARE_CYTRACKERSERCOM_HANDLER_H
#define FIRMWARE_CYTRACKERSERCOM_HANDLER_H

#include <CyTrackerParser.h>

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

//override of RH_MESH_MAX_MESSAGE_LEN to 150 for insurance of
#define RH_MESH_MAX_MESSAGE_LEN 150

#endif //FIRMWARE_CYTRACKERSERCOM_HANDLER_H
