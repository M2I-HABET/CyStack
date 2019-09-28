# Simple demo of sending and recieving data with the RFM95 LoRa radio.
# Author: Tony DiCola
import board
import busio
import digitalio
import time
import adafruit_rfm9x
import adafruit_ssd1306
import math
import adafruit_gps


def getpos(array):
    lat = array[3][:2]+str(float(array[3][2:])/60)[1:]
    lon = array[5][:3]+str(float(array[5][3:])/60)[1:]
    alt = array[10]
    return lat, lon, alt

def getBearing(latA,lonA,altA,latB,lonB,altB):
    phi1 = float(latA)*math.pi/180
    phi2 = float(latB)*math.pi/180
    dphi = float(latB-latA)*math.pi/180
    dlamb = float(lonB-lonA)*math.pi/180

    a = math.sin(dphi/2)*math.sin(dphi/2)+math.cos(phi1)*math.cos(phi2)*math.sin(dlamb/2)*math.sin(dlamb/2)

    c = 2*math.atan(math.sqrt(a)/math.sqrt(1-a))
    distance = R*c

    x = math.cos(latB*math.pi/180)*math.sin(math.pi/180*(lonA-lonB))
    y = math.cos(latA*math.pi/180)*math.sin(math.pi/180*latB)-math.sin(math.pi/180*latA)*math.cos(math.pi/180*latB)*math.cos(math.pi/180*(lonA-lonB))

    az =  -180/math.pi*math.atan(x/y)
    dla = float(latB)-float(latA)
    dlo = float(lonB)-float(lonA)
    print(az)
    #print("az"+str(az))
    print(dla)
    print(dlo)


    el = 180/math.pi*math.atan(int(altB-altA)/distance)
    #print(alt)
    #print(home_alt)
    print("el")
    print(el)
    print("az")
    print(az)
    print("distance:")
    print(distance)
    if(el<0):
        el = 0
    return

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
                        # module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D10)
RESET = digitalio.DigitalInOut(board.D11)
# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
# Initialize oled display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

# Send a packet.  Note you can only send a packet up to 252 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.

# Set up gps

RX = board.RX
TX = board.TX
uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
#gps = adafruit_gps.GPS(uart, debug=False)
#gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
#gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()

print('Waiting for packets...')

oled.fill(0)
oled.text('Hello', 0, 0, 1)
#oled.text('World', 0, 10, 1)
oled.show()
while True:
    packet = rfm9x.receive(timeout=1)
    # Optionally change the receive timeout from its default of 0.5 seconds:
    #packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    #gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        #if not gps.has_fix:
            # Try again if we don't have a fix yet.
        #    print('Waiting for fix...')
        #oled.fill(0)
        #oled.text(str(gps.latitude), 0, 0, 1)
        #oled.text(str(gps.longitude), 0, 10, 1)
        #oled.text(str(gps.altitude_m), 0, 20, 1)
        #oled.show()
    gps_string = uart.readline()
    print(gps_string)
    try:

        packet_text = "1,"+str(gps_string, 'ascii')
        packetArray = packet_text.split(",")
        lat, lon, alt = getpos(packetArray)
        oled.fill(0)
        oled.text(lat, 0, 0, 1)
        oled.text(lon, 0, 10, 1)
        oled.text(alt, 0, 20, 1)
        oled.show()
    except:
        continue
    continue
    if packet is None:
        # Packet has not been received
        LED.value = False
        #print('Received nothing! Listening again...')
    else:
        # Received a packet!
        LED.value = True
        # Print out the raw bytes of the packet:
        #print('Received (raw bytes): {0}'.format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        try:
            rssi = rfm9x.rssi
            packet_text = str(packet, 'ascii')
            packetArray = packet_text.split(",")
            if "GPGGA" in packet_text:
                lat, lon, alt = getpos(packetArray)
                oled.fill(0)
                oled.text(lat, 0, 0, 1)
                oled.text(lon, 0, 10, 1)
                oled.text(alt, 0, 20, 1)
                oled.show()
        except Exception as e:
            oled.fill(0)
            oled.text("Node: NA", 0, 0, 1)
            oled.text("Bearing: NA", 0, 10, 1)
            oled.text("Range: NA", 0, 20, 1)
            oled.show()
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
    time.sleep(.1)