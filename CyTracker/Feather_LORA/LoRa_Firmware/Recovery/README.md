# Directory Purpose:
Holds firmware files for the Recovery vehicel's software.
## Platform Target:
Adafruit Featherwing LoRa 32u4 (433MHz variant)

# Included Files & Classes

## Mission_Control.ino:
Arduino file uploaded to micro controller.

## Data.cpp
Holds local microcontroller variables.

## Radio.cpp
Holds variables passed around via the 433MHz network. This class
is also responsible for synchronization and operation of the
radio node on the mission control designated Arduino LoRa.
