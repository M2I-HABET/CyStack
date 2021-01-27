//
// Created by Matt Kreul on 1/19/21.
//

#include "CyTrackerSERCOM_Handler.h"

/**
 * Char used to append to readString. Once a character is read from Serial2 it will be assigned to this.
 */
uint8_t appendChar;

/**
 * String which contains the location data.  Initialized here.  It is created by appending the appendChar variable when
 * it gets a value.
 */
uint8_t readString[RH_MESH_MAX_MESSAGE_LEN] = "";

/**
 * This is the created instance of the Uart protocol from the GPS to the TODO insert board name.  Notice that the input
 * pins are A3 and A2 for the TODO insert board name.  TODO figure out why we are using sercom4
 */
Uart Serial2(&sercom4, A3, A2, SERCOM_RX_PAD_1, UART_TX_PAD_0);

/**
 * Function to append characters to the string print out.  It will add 1 character at a time.  This is called in the
 * SERCOM4_2_Handler() function to append characters to the "readString" variable.  This helps protect the program from
 * buffer overflow.
 *
 * @param s
 *  string to append to
 * @param c
 *  character to append to string
 * @param max_len
 *  max length of the string (150 characters)
 */
void append(uint8_t* s, uint8_t c, uint8_t max_len) {
	//TODO consider changing this to operate on the global variables only
	int len = strlen((char*)s);
	if(len<max_len){// protects against buffer overflow //TODO consider changing this to len < RH_MESHMAX_MESSAGE_LEN
		s[len] = c;//add char (well uint8_t)
		s[len+1] = '\0';// need null terminator at end since overwritten in previous line
	}
}

/**
 * SERCOM handler that adds characters to the printout string.  It will read the character and then assign the value to
 * appendChar.  This is then appended to readString.
 */
void SERCOM4_2_Handler(){
	Serial2.IrqHandler();
	appendChar = Serial2.read();
	append(readString, appendChar, RH_MESH_MAX_MESSAGE_LEN);
	/*
	 * ok so this makes it so that we don't have to block on the main loop.
	 * when a char comes in it fires this interrupt. When it fires we save the char
	 * and add it to the read string. when you exit this handler you continue
	 * your code where you stopped prior to the interrupt
	 */
}

// Interrupt handler functions
void SERCOM4_0_Handler() {
	Serial2.IrqHandler();
}
void SERCOM4_1_Handler(){
	Serial2.IrqHandler();
}
void SERCOM4_3_Handler(){
	Serial2.IrqHandler();
}



