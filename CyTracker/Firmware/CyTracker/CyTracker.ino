// Created by Matthew Plewa
// Creation date: 12/6/2020
// Modified: 1/27/2021
// Bassed off of http://www.airspayce.com/mikem/arduino/RadioHead/rf22_mesh_client_8pde-example.html
// and also https://learn.adafruit.com/radio-featherwing/using-the-rfm-9x-radio

// watchdog timer has issues with serial when it restarts and can cause it to hang!!

#include <SPI.h>
#include <RH_RF95.h>
#include <RHMesh.h>
#include <Adafruit_SleepyDog.h>
#include <stdio.h>
#include <string.h>
#include "wiring_private.h" // pinPeripheral() function
#include <Adafruit_GPS.h>
// definitions for Serial2, appendChar, and readString as well as global defs and SERCOM handler functions
#include <CyTrackerSERCOM_Handler.h>

// Change to 434.0 or other frequency, must match RX's freq!
///#define RF95_FREQ 434.0 //commented out for easier access for users


// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
RHMesh manager(rf95,CLIENT_ADDRESS);
Adafruit_GPS GPS(&Serial2);

void setup(){
	pinMode(RFM95_RST, OUTPUT);
	digitalWrite(RFM95_RST, HIGH);
	
	//Start the serial port and make sure it's running
	Serial.begin(9600);
	while (!Serial) {
		delay(1);
	}
	
	GPS.begin(9600);
	pinPeripheral(A2, PIO_SERCOM_ALT);  // Assign SERCOM functionality to A2
	pinPeripheral(A3, PIO_SERCOM_ALT);  // Assign SERCOM functionality to A3
	
	delay(100);
	
	GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_GGAONLY);
	GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
	Serial.println("Feather LoRa TX Test!");
	
	// manual reset
	digitalWrite(RFM95_RST, LOW);
	delay(10);
	digitalWrite(RFM95_RST, HIGH);
	delay(10);
	
	while (!rf95.init()) {
		Serial.println("LoRa radio init failed");
		while (1);
	}
	Serial.println("LoRa radio init OK!");
	
	// Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
	if (!rf95.setFrequency(RF95_FREQ)) {
		Serial.println("setFrequency failed");
		while (1);
	}
	Serial.print("Set Freq to: ");
	Serial.println(RF95_FREQ);
	// Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
	
	// The default transmitter power is 13dBm, using PA_BOOST.
	// If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
	// you can set transmitter powers from 5 to 23 dBm:
	rf95.setTxPower(RFPOWER, false);
	
}

//TODO Do we need this?
int16_t packetnum = 0;  // packet counter, we increment per xmission
// Dont put this on the stack:
uint8_t buf[RH_MESH_MAX_MESSAGE_LEN];
//uint8_t * buf = (uint8_t*) malloc(sizeof(uint8_t) * RH_MESH_MAX_MESSAGE_LEN);


void loop(){
	if(appendChar == '\n'){
		/*
		 * this will look for the end of a string and then print it.
		 * This does not block the loop till you have a full string.
		 */
		appendChar = '\0';// have to set a to something other then \n to prevent it from reentering this conditional statement

		Serial.print((char*)readString);// dont need a print ln because it already has \n
		Serial.println("Sending to manager_mesh_server3");
		
		// Send a message to a rf22_mesh_server
		// A route to the destination will be automatically discovered.
		
		if (manager.sendtoWait(readString, sizeof(readString), SERVER3_ADDRESS) == RH_ROUTER_ERROR_NONE){
			// It has been reliably delivered to the next node.
			// Now wait for a reply from the ultimate server
			Serial.println("past send");
			uint8_t len = sizeof(buf);
			uint8_t from;
			int8_t received_rssi = rf95.lastRssi();
			if (manager.recvfromAckTimeout(buf, &len, 3000, &from)){
				Serial.print("got reply from : 0x");
				Serial.print(from, HEX);
				Serial.print(": ");
				Serial.println((char*)buf);
				Serial.print("Rssi:");
				Serial.println(received_rssi, DEC);
			}
			else{
				Serial.println("No reply, is rf22_mesh_server1, rf22_mesh_server2 and rf22_mesh_server3 running?");
			}
		}
		else{
			Serial.println("sendtoWait failed. Are the intermediate mesh servers running?");
		}
		
		memset(readString,0,sizeof readString);// time for a new string
		appendChar='\0';// have to set a to something other then \n to prevent it from reentering this conditional statement
	}
  delay(10);
}
