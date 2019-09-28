# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import time
import board
import busio
import digitalio

import adafruit_gps
import adafruit_rfm9x
 # Device ID
FEATHER_ID = b'1'

print("start up")
# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
# pylint: disable=c-extension-no-member
CS = digitalio.DigitalInOut(board.D10)
# pylint: disable=c-extension-no-member
RESET = digitalio.DigitalInOut(board.D11)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)


# Define radio frequency, MUST match gateway frequency.
RADIO_FREQ_MHZ = 433.0

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Set transmit power to max
rfm9x.tx_power = 23

# Define RX and TX pins for the board's serial port connected to the GPS.
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
RX = board.RX
TX = board.TX

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
uartPayload = busio.UART(board.A1, RX, baudrate=9600, timeout=30)
# for a computer, use the pyserial library for uart access
#import serial
#uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3000)

# Create a GPS module instance.
#gps = adafruit_gps.GPS(uart, debug=False)

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
#gps.send_command(b'PMTK314,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on just minimum info (RMC only, location):
#gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
#gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
#gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
#gps.send_command(b'PMTK220,1000')
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
#gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
#gps.send_command(b'PMTK220,500')

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

def sendMessage(message):
    #try:
        LED.value = True
        rfm9x.send(FEATHER_ID+b','+message)
        LED.value = False
    #except:
    #    print("Message failed to send")


while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    #gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    #if current - last_print >= 1.0:
    gps_string = uart.readline()
    if "GPGGA" in gps_string:
        print(gps_string)
        sendMessage(gps_string)
    time.sleep(.1)
    while False:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...')
            try:
                sendMessage("NONE")
            except:
                print("not sending")
                pass
            continue

        sendString = 'Lat,{0:.6f},'.format(gps.latitude)
        sendString = sendString + 'Lon,{0:.6f},'.format(gps.longitude)
        sendString = sendString + 'Alt,{} '.format(gps.altitude_m)
        sendMessage(sendString)