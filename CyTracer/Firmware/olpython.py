# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import board
import busio
import digitalio
import time
import adafruit_rfm9x
import adafruit_ssd1306
import math
import adafruit_gps
 # Device ID
FEATHER_ID = b'hh'


def getpos(array):
    print(array)
    try:
        lat = array[3][:2]+str(float(array[3][2:])/60)[1:]
        lon = array[5][:3]+str(float(array[5][3:])/60)[1:]
        alt = array[10]
        if(array[4] == "S"):
            lat = "-"+lat
        if(array[6] == "W"):
            lon = "-"+lon
        return str(lat), str(lon), str(alt)
    except:
        return str(None),str(None),str(None)

def getBearing(latA,lonA,altA,latB,lonB,altB):
    R = 6372.795477598*1000
    phi1 = float(latA)*math.pi/180
    phi2 = float(latB)*math.pi/180
    dphi = (float(latB)-float(latA))*math.pi/180
    dlamb = (float(lonB)-float(lonA))*math.pi/180

    a = math.sin(dphi/2)*math.sin(dphi/2)+math.cos(phi1)*math.cos(phi2)*math.sin(dlamb/2)*math.sin(dlamb/2)

    c = 2*math.atan(math.sqrt(a)/math.sqrt(1-a))
    distance = R*c

    x = math.cos(float(latB)*math.pi/180)*math.sin(math.pi/180*(float(lonA)-float(lonB)))
    y = math.cos(float(latA)*math.pi/180)*math.sin(math.pi/180*float(latB))-math.sin(math.pi/180*float(latA))*math.cos(math.pi/180*float(latB))*math.cos(math.pi/180*(float(lonA)-float(lonB)))

    try:
        az =  -180/math.pi*math.atan(x/y)
    except:
        return 0,0,0
    dla = float(latB)-float(latA)
    dlo = float(lonB)-float(lonA)
    az = abs(az)%90
    az1 = az
    if(dla<0 and dlo>0):
        az = 180-az
    if(dla<0 and dlo<0 and az<270):
        az = 180+az
    if(dla>0 and dlo<0 and (az<180 or az>270)):
        az = 360-az
    if(dla>0 and dlo>0 and (az<90 or az>180)):
        az = az
    print(latA)
    print(lonA)
    print("#"*10)
    print(az1)
    print(az)
    #print("az"+str(az))
    print("Lat:"+str(dla))
    print("Lon:"+str(dlo))
    print("#"*10)
    el = 180/math.pi*math.atan(int(float(altB)-float(altA))/distance)
    if(el<0):
        el = 0
    return distance, az, el





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
RADIO_FREQ_MHZ = 434.0

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
#uartPayload = busio.UART(board.A1, RX, baudrate=9600, timeout=30)
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
# Initialize oled display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)
oled.text('Hello', 0, 0, 1)
#oled.text('World', 0, 10, 1)
oled.show()
latA="0"
latB="0"
lonA="0"
lonB="0"
altA="0"
altB="0"
rng = 0
bearing = 0
el = 0
current = time.monotonic()
old = current
while True:
    new = False
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    #gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    packet = rfm9x.receive(timeout=.1)
    #if current - last_print >= 1.0:
    gps_string = uart.readline()
    if "GPGGA" in gps_string:
        new = True
        try:

            packet_text = str(FEATHER_ID,'ascii')+","+str(gps_string, 'ascii')
            packetArray = packet_text.split(",")
            latA, lonA, altA = getpos(packetArray)
        except Exception as e:
            print(e)
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
        #test = ''.join([chr(b) for b in packet])
        test = b""+packet
        print(test)
        try:
            rssi = rfm9x.rssi
            packet_text = str(packet, 'ascii')
            packetArray = packet_text.split(",")
            if "GPGGA" in packet_text:
                old = current
                new = True
                latB, lonB, altB = getpos(packetArray)
                print('GPSData,'+latB+','+lonB+','+altB)
        except Exception as e:
            continue
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
    if new:
        try:
            rng, bearing, el = getBearing(latA,lonA,altA,latB,lonB,altB)
        except:
            pass
    oled.fill(0)
    oled.text("R: "+str(rng)+"m T:"+str(int(current-old)) , 0, 0, 1)
    oled.text("B: "+str(bearing), 0, 10, 1)
    oled.text("E: "+str(el)+" A:"+str(altB), 0, 20, 1)
    oled.show()
    time.sleep(.1)