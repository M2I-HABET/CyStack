//
// Created by Matt Kreul on 1/19/21.
//

#include "CyTrackerSERCOM_Handler.h"

uint8_t appendChar;
uint8_t readString[RH_MESH_MAX_MESSAGE_LEN] = "";
Uart Serial2(&sercom4, A3, A2, SERCOM_RX_PAD_1, UART_TX_PAD_0);

/**
 * Function to append characters to the string print out.  It will add 1 character at a time.  This is called in the
 * SERCOM4_2_Handler() function to append characters to the "readString" variable.
 *
 * @param s
 *  string to append to
 * @param c
 *  character to append to string
 * @param max_len
 *  max length of the string (150 bytes)
 */
void append(uint8_t* s, uint8_t c, uint8_t max_len) {
	//TODO consider changing this to operate on the global variables only
	int len = strlen((char*)s);
	if(len<max_len){// protects against buffer overflow
		s[len] = c;//add char (well uint8_t)
		s[len+1] = '\0';// need null terminator at end since overwritten in previous line
	}
}

/**
 * SERCOM handler that adds characters to the printout string
 */
void SERCOM4_2_Handler(){
	Serial2.IrqHandler();
	appendChar = Serial2.read();
	append(readString, appendChar, RH_MESH_MAX_MESSAGE_LEN);
	/*
	 * ok so this make it so that we don't have to block on the main loop.
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



