EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:Feather U5
U 1 1 5FEC8213
P 4850 950
F 0 "U5" H 5300 1115 50  0000 C CNN
F 1 "M4" H 5300 1024 50  0000 C CNN
F 2 "Module:Adafruit_Feather_WithMountingHoles" H 5250 1100 50  0001 C CNN
F 3 "" H 5250 1100 50  0001 C CNN
	1    4850 950 
	1    0    0    -1  
$EndComp
$Comp
L Device:Feather U3
U 1 1 5FECAF4B
P 3050 950
F 0 "U3" H 3500 1115 50  0000 C CNN
F 1 "GPS Feather" H 3500 1024 50  0000 C CNN
F 2 "Module:Adafruit_Feather_WithMountingHoles" H 3450 1100 50  0001 C CNN
F 3 "" H 3450 1100 50  0001 C CNN
	1    3050 950 
	1    0    0    -1  
$EndComp
$Comp
L Device:Feather U1
U 1 1 5FECE996
P 1250 950
F 0 "U1" H 1700 1115 50  0000 C CNN
F 1 "LoRa Feather" H 1700 1024 50  0000 C CNN
F 2 "Module:Adafruit_Feather_WithMountingHoles" H 1650 1100 50  0001 C CNN
F 3 "" H 1650 1100 50  0001 C CNN
	1    1250 950 
	1    0    0    -1  
$EndComp
Text GLabel 4750 1200 0    50   Input ~ 0
Reset
$Comp
L power:GND #PWR0101
U 1 1 5FED0DF9
P 4750 1500
F 0 "#PWR0101" H 4750 1250 50  0001 C CNN
F 1 "GND" V 4755 1372 50  0000 R CNN
F 2 "" H 4750 1500 50  0001 C CNN
F 3 "" H 4750 1500 50  0001 C CNN
	1    4750 1500
	0    1    1    0   
$EndComp
$Comp
L power:+3.3V #PWR0102
U 1 1 5FED19B1
P 4750 1300
F 0 "#PWR0102" H 4750 1150 50  0001 C CNN
F 1 "+3.3V" V 4765 1428 50  0000 L CNN
F 2 "" H 4750 1300 50  0001 C CNN
F 3 "" H 4750 1300 50  0001 C CNN
	1    4750 1300
	0    -1   -1   0   
$EndComp
Text GLabel 4750 2200 0    50   Output ~ 0
SCK
Text GLabel 4750 2300 0    50   Output ~ 0
MOSI
Text GLabel 4750 2400 0    50   Input ~ 0
MISO
Text GLabel 2950 1200 0    50   Output ~ 0
Reset
$Comp
L power:+3.3V #PWR0103
U 1 1 5FED8F62
P 2950 1300
F 0 "#PWR0103" H 2950 1150 50  0001 C CNN
F 1 "+3.3V" V 2965 1428 50  0000 L CNN
F 2 "" H 2950 1300 50  0001 C CNN
F 3 "" H 2950 1300 50  0001 C CNN
	1    2950 1300
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5FED941E
P 2950 1500
F 0 "#PWR0104" H 2950 1250 50  0001 C CNN
F 1 "GND" V 2955 1372 50  0000 R CNN
F 2 "" H 2950 1500 50  0001 C CNN
F 3 "" H 2950 1500 50  0001 C CNN
	1    2950 1500
	0    1    1    0   
$EndComp
Text GLabel 1150 1200 0    50   Output ~ 0
Reset
$Comp
L power:+3.3V #PWR0105
U 1 1 5FED9F3B
P 1150 1300
F 0 "#PWR0105" H 1150 1150 50  0001 C CNN
F 1 "+3.3V" V 1165 1428 50  0000 L CNN
F 2 "" H 1150 1300 50  0001 C CNN
F 3 "" H 1150 1300 50  0001 C CNN
	1    1150 1300
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5FEDAB87
P 1150 1500
F 0 "#PWR0106" H 1150 1250 50  0001 C CNN
F 1 "GND" V 1155 1372 50  0000 R CNN
F 2 "" H 1150 1500 50  0001 C CNN
F 3 "" H 1150 1500 50  0001 C CNN
	1    1150 1500
	0    1    1    0   
$EndComp
Text GLabel 1150 2200 0    50   Input ~ 0
SCK
Text GLabel 1150 2300 0    50   Input ~ 0
MOSI
Text GLabel 1150 2400 0    50   Output ~ 0
MISO
Text GLabel 2250 2200 2    50   Input ~ 0
CS1
Text GLabel 5850 2200 2    50   Output ~ 0
CS1
$Comp
L power:+3.3V #PWR0107
U 1 1 5FEE34BF
P 4650 4350
F 0 "#PWR0107" H 4650 4200 50  0001 C CNN
F 1 "+3.3V" H 4665 4523 50  0000 C CNN
F 2 "" H 4650 4350 50  0001 C CNN
F 3 "" H 4650 4350 50  0001 C CNN
	1    4650 4350
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5FEE4590
P 4550 4150
F 0 "#PWR0108" H 4550 3900 50  0001 C CNN
F 1 "GND" H 4555 3977 50  0000 C CNN
F 2 "" H 4550 4150 50  0001 C CNN
F 3 "" H 4550 4150 50  0001 C CNN
	1    4550 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4650 4150 4650 4350
Text GLabel 4450 4350 3    50   Input ~ 0
Transmit
Wire Wire Line
	4450 4350 4450 4150
Text GLabel 4350 4150 3    50   Output ~ 0
Recieve
Text GLabel 4250 4150 3    50   Output ~ 0
GPS_Fix
$Comp
L Device:GPS_Breakout U4
U 1 1 5FEE2186
P 3900 3550
F 0 "U4" H 4828 3288 50  0000 L CNN
F 1 "GPS_Breakout" H 4828 3197 50  0000 L CNN
F 2 "Devices:GPS_Breakout" H 4350 3650 50  0001 C CNN
F 3 "" H 4350 3650 50  0001 C CNN
	1    3900 3550
	1    0    0    -1  
$EndComp
$Comp
L Device:LoRa_Breakout U2
U 1 1 5FEED44E
P 2200 3600
F 0 "U2" H 3128 3421 50  0000 L CNN
F 1 "LoRa_Breakout" H 3128 3330 50  0000 L CNN
F 2 "Devices:LoRa_Breakout" H 2650 4150 50  0001 C CNN
F 3 "" H 2650 4150 50  0001 C CNN
	1    2200 3600
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0109
U 1 1 5FEEE881
P 2250 4150
F 0 "#PWR0109" H 2250 4000 50  0001 C CNN
F 1 "+3.3V" H 2265 4323 50  0000 C CNN
F 2 "" H 2250 4150 50  0001 C CNN
F 3 "" H 2250 4150 50  0001 C CNN
	1    2250 4150
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 5FEEED44
P 2350 4350
F 0 "#PWR0110" H 2350 4100 50  0001 C CNN
F 1 "GND" H 2355 4177 50  0000 C CNN
F 2 "" H 2350 4350 50  0001 C CNN
F 3 "" H 2350 4350 50  0001 C CNN
	1    2350 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2350 4150 2350 4350
Text GLabel 2650 4150 3    50   Input ~ 0
SCK
Text GLabel 2750 4150 3    50   Output ~ 0
MISO
Text GLabel 2850 4150 3    50   Input ~ 0
MOSI
Text GLabel 2950 4150 3    50   Input ~ 0
CS1
Text GLabel 5850 2600 2    50   Output ~ 0
SCL
Text GLabel 5850 2700 2    50   Input ~ 0
SDA
$Comp
L power:+5V #PWR0111
U 1 1 5FF4AD72
P 5850 1800
F 0 "#PWR0111" H 5850 1650 50  0001 C CNN
F 1 "+5V" V 5865 1928 50  0000 L CNN
F 2 "" H 5850 1800 50  0001 C CNN
F 3 "" H 5850 1800 50  0001 C CNN
	1    5850 1800
	0    1    1    0   
$EndComp
Text GLabel 4750 1800 0    50   Output ~ 0
Transmit
Text GLabel 4750 1900 0    50   Input ~ 0
Recieve
Text GLabel 2950 2600 0    50   Output ~ 0
Recieve
Text GLabel 2950 2500 0    50   Input ~ 0
Transmit
$Comp
L power:+5V #PWR0112
U 1 1 6045E758
P 6750 1000
F 0 "#PWR0112" H 6750 850 50  0001 C CNN
F 1 "+5V" V 6765 1128 50  0000 L CNN
F 2 "" H 6750 1000 50  0001 C CNN
F 3 "" H 6750 1000 50  0001 C CNN
	1    6750 1000
	0    -1   -1   0   
$EndComp
Text GLabel 6750 1100 0    50   Output ~ 0
3V3power
$Comp
L power:GND #PWR0113
U 1 1 604793E9
P 6750 1200
F 0 "#PWR0113" H 6750 950 50  0001 C CNN
F 1 "GND" V 6755 1072 50  0000 R CNN
F 2 "" H 6750 1200 50  0001 C CNN
F 3 "" H 6750 1200 50  0001 C CNN
	1    6750 1200
	0    1    1    0   
$EndComp
Text GLabel 6750 1300 0    50   Input ~ 0
PayloadEnable
$Comp
L Connector:Conn_01x06_Female J1
U 1 1 6067946D
P 6950 1200
F 0 "J1" H 6978 1176 50  0000 L CNN
F 1 "Conn_01x06_Female" H 6978 1085 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 6950 1200 50  0001 C CNN
F 3 "~" H 6950 1200 50  0001 C CNN
	1    6950 1200
	1    0    0    -1  
$EndComp
$EndSCHEMATC
