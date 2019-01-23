# Directory Purpose
Holds all dependencies to run LoRa_Payload's firmware.

# Included Files:

## LoRa_Payload
Arduino sketch uploaded to micro controller. High-level interactions
between the various classes.

## Data.cpp
Holds all variables native to the LoRa_Payload.

## GPS.cpp
Responsible for retrieving and formatting the GPS data into Data.cpp's variables.

## Radio.cpp
Holds variables passed around via the 433MHz network. This class
is also responsible for synchronization and operation of the 
radio node on the payload designated Arduino LoRa. 