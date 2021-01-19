//
// Created by Matt Kreul on 1/19/21.
//

#ifndef FIRMWARE_CYTRACKERPARSER_H
#define FIRMWARE_CYTRACKERPARSER_H

#include <stdint.h>
#include <string.h>

void append(uint8_t* s, uint8_t c, uint8_t max_len) {
	int len = strlen((char*)s);
	if(len<max_len){// protects against buffer overflow
		s[len] = c;//add char (well uint8_t)
		s[len+1] = '\0';// need null terminator at end since overwritten in previous line
	}
}

#endif //FIRMWARE_CYTRACKERPARSER_H
