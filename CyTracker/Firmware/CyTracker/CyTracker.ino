// Created by Matthew Plewa
// Creation date: 12/6/2020
// Modified: 12/7/2020
// Bassed off of http://www.airspayce.com/mikem/arduino/RadioHead/rf22_mesh_client_8pde-example.html
// and also https://learn.adafruit.com/radio-featherwing/using-the-rfm-9x-radio


// watchdog timer has issues with serial when it restarts and can cause it to hang!!

#include <SPI.h>
#include <RH_RF95.h>
#include <RHMesh.h>
#include <Adafruit_SleepyDog.h>
#include <stdio.h>
#include <String.h>
#include "wiring_private.h" // pinPeripheral() function
#include <Adafruit_GPS.h>
// ALL DEFINES BELLOW

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
// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
RHMesh manager(rf95,CLIENT_ADDRESS);
Uart Serial2 (&sercom4, A3, A2, SERCOM_RX_PAD_1, UART_TX_PAD_0);
Adafruit_GPS GPS(&Serial2);

#define RH_MESH_MAX_MESSAGE_LEN 150
uint8_t readString[RH_MESH_MAX_MESSAGE_LEN]="";
uint8_t readStringClean[RH_MESH_MAX_MESSAGE_LEN]="";
uint8_t a;

void SERCOM4_0_Handler()                // Interrupt handler functions
{
	Serial2.IrqHandler();
	
}
void SERCOM4_1_Handler()
{
	Serial2.IrqHandler();
	
}
void SERCOM4_2_Handler()
{
	Serial2.IrqHandler();
	a = Serial2.read();
	append(readString,a,RH_MESH_MAX_MESSAGE_LEN);
	/*
	 * ok so this make it so that we don't have to block on the main loop.
	 * when a char comes in it fires this interrupt. When it fires we save the char
	 * and add it to the read string. when you exit this handler you continue
	 * your code where you stopped prior to the interrupt
	 */
}
void SERCOM4_3_Handler()
{
	Serial2.IrqHandler();
}



void append(uint8_t* s, uint8_t c, uint8_t max_len) {
	int len = strlen((char*)s);
	if(len<max_len){// protects against buffer overflow
		s[len] = c;//add char (well uint8_t)
		s[len+1] = '\0';// need null terminator at end since overwritten in previous line
	}
}


void setup()
{
	pinMode(RFM95_RST, OUTPUT);
	digitalWrite(RFM95_RST, HIGH);
	
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

int16_t packetnum = 0;  // packet counter, we increment per xmission
//uint8_t data[] = "Hello World!";
// Dont put this on the stack:
uint8_t buf[RH_MESH_MAX_MESSAGE_LEN];
//int iterate = 0;
void loop(){
//  Serial.print("Looped ");
//  Serial.print( iterate);
//  Serial.println(" times");
	if(a=='\n'){
		/*
		 * this will look for the end of a string and then print it.
		 * This does not block the loop till you have a full string.
		 */
		a='\0';// have to set a to something other then \n to prevent it from reentering this conditional statement
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
		else
			Serial.println("sendtoWait failed. Are the intermediate mesh servers running?");
		
		memset(readString,0,sizeof readString);// time for a new string
		a='\0';// have to set a to something other then \n to prevent it from reentering this conditional statement
	}

//  delay(10);
//  iterate++;

}
